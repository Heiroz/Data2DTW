from scapy.all import rdpcap, IP
import pandas as pd
import os
from datetime import datetime, timezone

def generate_time_series(pcap_file, output_file, resample_interval='50ms', max_len = 120, min_lens = 110):
    packets = rdpcap(pcap_file)
    time_stamps = []
    base_time = None

    for packet in packets:
        if IP in packet:
            packet_time = datetime.fromtimestamp(float(packet.time), timezone.utc)
            if base_time is None:
                base_time = packet_time
            elapsed_time = (packet_time - base_time).total_seconds() * 1000
            packet_size = len(packet)
            time_stamps.append((elapsed_time, packet_size))

    df = pd.DataFrame(time_stamps, columns=['ElapsedTime', 'PacketSize'])
    
    resample_interval_ms = pd.to_timedelta(resample_interval).total_seconds() * 1000
    df['ElapsedTime'] = (df['ElapsedTime'] // resample_interval_ms * resample_interval_ms).astype(int)
    
    df_grouped = df.groupby('ElapsedTime').sum()

    if not df_grouped.empty:
        max_time = df_grouped.index.max()
        complete_index = range(0, int(max_time + resample_interval_ms), int(resample_interval_ms))
        df_grouped = df_grouped.reindex(complete_index, fill_value=0)

    if min_lens < len(df_grouped) < max_len:
        df_grouped.to_csv(output_file)

def process(folder_path, output_folder, resample_interval='50ms', max_len = 120, min_lens = 110):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pcap"):
            pcap_path = os.path.join(folder_path, filename)
            output_file = os.path.join(output_folder, f"{filename[:-5]}_time_series.csv")
            generate_time_series(pcap_path, output_file, resample_interval, max_len, min_lens)