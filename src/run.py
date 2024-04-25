import flow_raw
import flow_syn
import timeseries_raw
import timeseries_syn
import dtw
import show_dtw

raw_file = "../data_in/raw.pcap"
syn_file = "../data_in/syn.csv"
raw_flow_folder = "../data_flow/flow_raw"
syn_flow_folder = "../data_flow/flow_syn"
raw_timeseries_folder = "../data_timeseries/timeseries_raw"
syn_timeseries_folder = "../data_timeseries/timeseries_syn"
dtw_folder = "../caida_dtw"
dtw_file = "../caida_dtw.csv"
image_folder = "../caida_dtw_image"

flow_raw.process(raw_file, raw_flow_folder)
flow_syn.process(syn_file, syn_flow_folder)
timeseries_raw.process(raw_flow_folder, raw_timeseries_folder, '20ms', 500, 100)
timeseries_syn.process(syn_flow_folder, syn_timeseries_folder, '20ms', 500, 100)
dtw.process(syn_timeseries_folder, raw_timeseries_folder, dtw_folder, dtw_file)
show_dtw.generate(dtw_file, dtw_folder, image_folder, 100)