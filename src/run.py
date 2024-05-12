import flow_raw
import flow_syn
import timeseries_raw
import timeseries_syn
import dtw
import show_dtw
raw_file = "../data_in/video_raw.pcap"
syn_file = "../data_in/video_syn.csv"
raw_flow_folder = "../data_flow/video_raw"
syn_flow_folder = "../data_flow/video_syn"
raw_timeseries_folder = "../data_timeseries/video_raw"
syn_timeseries_folder = "../data_timeseries/video_syn"
dtw_folder = "../dtw_file/video_dtw"
dtw_file = "../dtw/video_dtw.csv"
image_folder = "../image/video_dtw_image"
min_packet_len = 400
min_flow_len = 1
max_flow_len = 80000
interval = '10000ms'

flow_raw.process(raw_file, raw_flow_folder, min_packet_len)
flow_syn.process(syn_file, syn_flow_folder, min_packet_len)
timeseries_raw.process(raw_flow_folder, raw_timeseries_folder, interval, max_flow_len, min_flow_len)
timeseries_syn.process(syn_flow_folder, syn_timeseries_folder, interval, max_flow_len, min_flow_len)
dtw.process(syn_timeseries_folder, raw_timeseries_folder, dtw_folder, dtw_file)
show_dtw.generate(dtw_file, dtw_folder, image_folder, 14)
