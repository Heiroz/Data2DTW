import pandas as pd
import os
import fastdtw
from scipy.spatial.distance import euclidean

def read_and_process(file_path):
    data = pd.read_csv(file_path)
    if 'ElapsedTime' in data.columns and 'PacketSize' in data.columns:
        data.rename(columns={'ElapsedTime': 'time', 'PacketSize': 'flow'}, inplace=True)
    elif 'time' in data.columns and 'pkt_len' in data.columns:
        data.rename(columns={'pkt_len': 'flow'}, inplace=True)
    return data

def find_most_similar(synthetic, actual_files):
    best_distance = float('inf')
    best_match = None
    for actual_file in actual_files:
        actual_data = read_and_process(actual_file)
        if not synthetic.empty and not actual_data.empty:
            distance, path = fastdtw(synthetic[['time', 'flow']], actual_data[['time', 'flow']], dist=euclidean)
            distance = distance / max(len(synthetic), len(actual_data))
            if distance < best_distance:
                best_distance = distance
                best_match = actual_file
    return best_match, best_distance

def process(synthetic_folder, actual_folder, output_folder, summary_file):
    synthetic_files = [os.path.join(synthetic_folder, f) for f in os.listdir(synthetic_folder) if f.endswith('.csv')]
    actual_files = [os.path.join(actual_folder, f) for f in os.listdir(actual_folder) if f.endswith('.csv')]
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    correlations = []
    for synthetic_file in synthetic_files:
        best_match, best_distance = find_most_similar(read_and_process(synthetic_file), actual_files)
        if best_match:
            synthetic_data = read_and_process(synthetic_file)
            actual_data = read_and_process(best_match)
            merged = synthetic_data.merge(actual_data, on='time', suffixes=('_synthetic', '_actual'))
            output_file = os.path.join(output_folder, f"merged_{os.path.basename(synthetic_file)}")
            merged.to_csv(output_file, index=False)
            correlations.append({
                'Synthetic File': os.path.basename(synthetic_file),
                'Best Match': os.path.basename(best_match),
                'DTW Distance': best_distance
            })
            print(f"Merged data saved to {output_file} with DTW Distance {best_distance}")

    df_correlations = pd.DataFrame(correlations)
    df_correlations.to_csv(summary_file, index=False)
    print(f"Correlation summary saved to {summary_file}")