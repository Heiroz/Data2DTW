import pandas as pd
import os

def process(input_folder, output_folder, time_window='50ms', max_len = 230, min_lens = 220):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    time_delta_ms = pd.to_timedelta(time_window).total_seconds() * 1000
    
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
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue
            
            data['ElapsedTime'] = (data['ElapsedTime'] - data['ElapsedTime'].min()).astype('timedelta64[ms]') / time_delta_ms
            data['ElapsedTime'] = data['ElapsedTime'].astype(int) * int(time_delta_ms)
            
            total_traffic = data.groupby('ElapsedTime')['PacketSize'].sum()
            
            if not total_traffic.empty:
                max_time = total_traffic.index.max()
                complete_index = pd.RangeIndex(start=0, stop=max_time + time_delta_ms, step=time_delta_ms)
                total_traffic = total_traffic.reindex(complete_index, fill_value=0)
            
            if min_lens < len(total_traffic) < max_len:
                output_file_path = os.path.join(output_folder, f"processed_{filename}")
                total_traffic.to_csv(output_file_path, header=True, index_label='ElapsedTime')