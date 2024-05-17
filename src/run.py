import flow_raw
import flow_syn
import timeseries_raw
import timeseries_syn
import my_dtw
import show_dtw
raw_file = "../data_in/imc_dc_raw.pcap"
syn_file = "../data_in/imc_dc_syn.csv"
raw_flow_folder = "../data_flow/imc_dc_raw"
syn_flow_folder = "../data_flow/imc_dc_syn"
raw_timeseries_folder = "../data_timeseries/imc_dc_raw"
syn_timeseries_folder = "../data_timeseries/imc_dc_syn"
segment_length = '10s'
resample_interval = '100ms'
non_zero_num = 20
dtw_folder = "../dtw_file/imc_dc_dtw"
dtw_file = "../dtw/imc_dc_dtw.csv"
image_folder = "../image/imc_dc_dtw_image"
min_packet_len = 100
image_num = 100
flow_raw.process(raw_file, raw_flow_folder, min_packet_len)
flow_syn.process(syn_file, syn_flow_folder, min_packet_len)
<<<<<<< HEAD
timeseries_raw.process(raw_flow_folder, raw_timeseries_folder, interval, max_flow_len, min_flow_len)
timeseries_syn.process(syn_flow_folder, syn_timeseries_folder, interval, max_flow_len, min_flow_len)
dtw.process(syn_timeseries_folder, raw_timeseries_folder, dtw_folder, dtw_file)
show_dtw.generate(dtw_file, dtw_folder, image_folder, 14)
=======
timeseries_raw.process(raw_flow_folder, raw_timeseries_folder, segment_length, resample_interval, non_zero_num)
timeseries_syn.process(syn_flow_folder, syn_timeseries_folder, segment_length, resample_interval, non_zero_num)
my_dtw.process(syn_timeseries_folder, raw_timeseries_folder, dtw_folder, dtw_file)
show_dtw.generate_images(dtw_folder, image_folder, image_num)
>>>>>>> e4a096630865c6029f82b96620ce10c10645efb8
