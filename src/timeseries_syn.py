import pandas as pd
import os

def generate_time_series(input_folder, output_folder, segment_length='3s', resample_interval='100ms', non_zero_num=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    series_counter = 1
    segment_length_ms = pd.to_timedelta(segment_length).total_seconds() * 1000
    time_delta_ms = pd.to_timedelta(resample_interval).total_seconds() * 1000

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            
            if 'time' in data.columns and 'pkt_len' in data.columns:
                data.rename(columns={'time': 'ElapsedTime', 'pkt_len': 'PacketSize'}, inplace=True)
            else:
                continue
            
            try:
                data['ElapsedTime'] = pd.to_datetime(data['ElapsedTime'])
                data['ElapsedTime'] = (data['ElapsedTime'] - data['ElapsedTime'].min()).dt.total_seconds() * 1000
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue
            
            # Resample and sum up the packet sizes for each interval
            data.set_index(pd.to_timedelta(data['ElapsedTime'], unit='ms'), inplace=True)
            data_resampled = data['PacketSize'].resample(resample_interval).sum().fillna(0)
            
            # Convert the index to milliseconds
            data_resampled.index = (data_resampled.index.total_seconds() * 1000).astype(int)

            # Segment the data into 3-second chunks
            num_segments = int(data_resampled.index.max() // segment_length_ms) + 1

            for i in range(num_segments):
                segment_start = i * segment_length_ms
                segment_end = segment_start + segment_length_ms
                segment = data_resampled[(data_resampled.index >= segment_start) & (data_resampled.index < segment_end)]
                
                # Reset index to start from 0 for each segment
                if not segment.empty:
                    segment.index = segment.index - segment.index.min()
                
                # Check the amount of zero intervals
                if (len(segment) - segment.isin([0]).sum()) > non_zero_num:
                    segment_file = os.path.join(output_folder, f"timeseries_{series_counter}.csv")
                    segment.to_csv(segment_file, header=True, index_label='ElapsedTime')
                    series_counter += 1

def process(input_folder, output_folder):
    generate_time_series(input_folder, output_folder)
