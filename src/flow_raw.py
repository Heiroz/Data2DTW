from scapy.all import rdpcap, wrpcap, IP, TCP, UDP
import os

def process(pcap_file, output_dir, packet_len):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    packets = rdpcap(pcap_file)
    flows = {}

    for packet in packets:
        if IP in packet:
            srcip = packet[IP].src
            dstip = packet[IP].dst
            proto = packet[IP].proto
            srcport = dstport = None
            if TCP in packet or UDP in packet:
                srcport = packet.sport
                dstport = packet.dport

            flow_id = f"{srcip}_{dstip}_{srcport}_{dstport}_{proto}"

            if flow_id not in flows:
                flows[flow_id] = []
            flows[flow_id].append(packet)

    for flow_id, packets in flows.items():
        if len(packets) > packet_len:
            sorted_packets = sorted(packets, key=lambda x: x.time)
            filename = os.path.join(output_dir, f"{flow_id.replace(':', '_').replace('|', '_').replace('/', '_').replace(' ', '_')}.pcap")
            wrpcap(filename, sorted_packets)