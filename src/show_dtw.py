import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate(data_csv_path, base_path, output_folder, sample_num):
    df = pd.read_csv(data_csv_path)

    necessary_columns = ['Synthetic File', 'DTW Distance']
    if not all(column in df.columns for column in necessary_columns):
        raise ValueError("Dataframe does not contain all necessary columns.")

    sampled_files = df.sample(n=sample_num, random_state=1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, row in sampled_files.iterrows():
        synthetic_filename = f"merged_{row['Synthetic File']}"
        synthetic_file_path = os.path.join(base_path, synthetic_filename)

        if os.path.exists(synthetic_file_path):
            synthetic_data = pd.read_csv(synthetic_file_path)

            plt.figure(figsize=(20, 6))
            plt.plot(synthetic_data['time'], synthetic_data['flow_synthetic'], label='Synthetic Flow', marker='o', linestyle='-')
            plt.plot(synthetic_data['time'], synthetic_data['flow_actual'], label='Actual Flow', marker='o', linestyle='-')
            plt.xlabel('Time(ms)')
            plt.ylabel('Bytes')
            plt.title(f"Time Series Data for {synthetic_filename}")
            plt.legend()
            plt.grid(False)
            
            graph_filename = f"Comparison_{index}.png"
            plt.savefig(os.path.join(output_folder, graph_filename))
            plt.close()
        else:
            print(f"File not found: {synthetic_file_path}")

    plt.figure(figsize=(10, 6))
    plt.scatter(range(sample_num), sampled_files['DTW Distance'])
    plt.xlabel('Sample Index')
    plt.ylabel('DTW Distance')
    plt.title('Scatter Plot of DTW Distances')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'DTW_Distance_Scatter.png'))
    plt.close()