from scapy.all import rdpcap, IP
import pandas as pd
import os
from datetime import datetime, timezone

def generate_time_series(pcap_file, output_folder, series_counter, segment_length='3s', resample_interval='100ms', non_zero_num=5):
    packets = rdpcap(pcap_file)
    time_stamps = []
    base_time = None

    for packet in packets:
        if IP in packet:
            packet_time = datetime.fromtimestamp(float(packet.time), timezone.utc)
            if base_time is None:
                base_time = packet_time
            elapsed_time = (packet_time - base_time).total_seconds() * 1000  # milliseconds
            packet_size = len(packet)
            time_stamps.append((elapsed_time, packet_size))

    df = pd.DataFrame(time_stamps, columns=['ElapsedTime', 'PacketSize'])
    
    # Resample and sum up the packet sizes for each interval
    df.set_index(pd.to_timedelta(df['ElapsedTime'], unit='ms'), inplace=True)
    df_resampled = df['PacketSize'].resample(resample_interval).sum().fillna(0)
    
    # Convert the index to milliseconds and adjust from zero
    df_resampled.index = (df_resampled.index.total_seconds() * 1000).astype(int)
    df_resampled.index -= df_resampled.index.min()

    # Segment the data into 3-second chunks
    segment_length_ms = pd.to_timedelta(segment_length).total_seconds() * 1000
    num_segments = int(df_resampled.index.max() // segment_length_ms) + 1

    for i in range(num_segments):
        segment_start = i * segment_length_ms
        segment_end = segment_start + segment_length_ms
        segment = df_resampled[(df_resampled.index >= segment_start) & (df_resampled.index < segment_end)]
        if not segment.empty:
            segment.index = segment.index - segment.index.min()
        if len(segment) - segment.isin([0]).sum() > non_zero_num:
            segment_file = os.path.join(output_folder, f"timeseries_{series_counter}.csv")
            segment.to_csv(segment_file, header=True)
            series_counter += 1
    return series_counter

def process(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    series_counter = 1
    for filename in os.listdir(folder_path):
        if filename.endswith(".pcap"):
            pcap_path = os.path.join(folder_path, filename)
            series_counter = generate_time_series(pcap_path, output_folder, series_counter)

