import flow_raw
import flow_syn
import timeseries_raw
import timeseries_syn
import dtw
import show_dtw
file_name = "video"
raw_file = "../data_in/{file_name}_raw.pcap"
syn_file = "../data_in/{file_name}_syn.csv"
raw_flow_folder = "../data_flow/{file_name}_raw"
syn_flow_folder = "../data_flow/{file_name}_syn"
raw_timeseries_folder = "../data_timeseries/{file_name}_raw"
syn_timeseries_folder = "../data_timeseries/{file_name}_syn"
dtw_folder = "../{file_name}_dtw"
dtw_file = "../{file_name}_dtw.csv"
image_folder = "../{file_name}_dtw_image"

flow_raw.process(raw_file, raw_flow_folder)
flow_syn.process(syn_file, syn_flow_folder)
# timeseries_raw.process(raw_flow_folder, raw_timeseries_folder, '2000ms', 50000, 100)
# timeseries_syn.process(syn_flow_folder, syn_timeseries_folder, '2000ms', 50000, 100)
# dtw.process(syn_timeseries_folder, raw_timeseries_folder, dtw_folder, dtw_file)
show_dtw.generate(dtw_file, dtw_folder, image_folder, 30)