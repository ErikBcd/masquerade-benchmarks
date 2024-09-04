import json
from os import listdir, path
import os
from os.path import isfile, join
import re

import pandas as pd
import matplotlib.pyplot as plt

class Iperf3DataTCP:
    def __init__(self):
        self.sent_bps = 0
        self.sent_bytes = 0
        
        self.received_bps = 0
        self.received_bytes = 0
        self.retransmits = 0
        
        self.is_sender = False
        
        self.cpu_host_total = 0
        self.cpu_host_system = 0
        self.cpu_remote_system = 0
        
        self.target_bitrate = 0
        self.protocol = ""
        self.num_streams = 0
        self.duration = 0
        
        self.cookie = ""
        
    def parse(self, jsonfile):
        self.sent_bps           = jsonfile['end']['sum_sent']['bits_per_second']
        self.sent_bytes         = jsonfile['end']['sum_sent']['bytes']
        
        self.received_bps       = jsonfile['end']['sum_received']['bits_per_second']
        self.received_bytes     = jsonfile['end']['sum_received']['bytes']
        
        self.is_sender          = jsonfile['end']['sum_received']['sender']
        
        self.cpu_host_total     = jsonfile['end']['cpu_utilization_percent']['host_total']
        self.cpu_host_system    = jsonfile['end']['cpu_utilization_percent']['host_total']
        self.cpu_remote_system  = jsonfile['end']['cpu_utilization_percent']['remote_system']
        
        self.target_bitrate     = jsonfile['start']['target_bitrate']
        self.protocol           = jsonfile['start']['test_start']['protocol']
        self.num_streams        = jsonfile['start']['test_start']['num_streams']
        self.duration           = jsonfile['start']['test_start']['duration']
        self.cookie             = jsonfile['start']['cookie']
    
    def print_data(self):
        print("Sent BPS          = " + "{:.3f}".format(self.sent_bps / 1000000) + " Mbits")
        print("Sent bytes        = " + str(self.sent_bytes / 10000) + " Mbytes")
        print("Retransmits       = " + str(self.retransmits))
        print("Received BPS      = " + "{:.3f}".format(self.received_bps / 1000000) + " Mbits")
        print("Received bytes    = " + str(self.received_bytes / 10000) + " Mbytes")
        print("CPU Host total    = " + "{:.2f}".format(self.cpu_host_total) + "%")
        print("CPU Host system   = " + "{:.2f}".format(self.cpu_host_system) + "%")
        print("CPU Remote system = " + "{:.2f}".format(self.cpu_remote_system) + "%")
        print("Target Bitrate    = " + str(self.target_bitrate / 1000000) + " Mbit/s")
        print("Protocol          = " + self.protocol)
        print("Parallel          = " + str(self.num_streams))
        print("Duration          = " + str(self.duration) + "s")
        print("Cookie            = " + self.cookie)
 
 
class Iperf3DataUDP:
    def __init__(self):
        self.sent_bps = 0
        self.sent_bytes = 0
        self.sent_jitter = 0.0
        self.sent_lost_packets = 0
        self.sent_packets = 0
        
        self.received_bps = 0
        self.received_bytes = 0
        self.received_jitter = 0.0
        self.received_lost_packets = 0
        self.received_packets = 0
        
        self.cpu_host_total = 0
        self.cpu_host_system = 0
        self.cpu_remote_system = 0
        self.target_bitrate = 0
        self.protocol = ""
        self.num_streams = 0
        self.duration = 0
        self.cookie = ""
        self.sender = False
        
    def parse(self, jsonfile):
        self.sent_bps               = jsonfile['end']['sum_sent']['bits_per_second']
        self.sent_bytes             = jsonfile['end']['sum_sent']['bytes']
        self.sent_jitter            = jsonfile['end']['sum_sent']['jitter_ms']
        self.sent_lost_packets      = jsonfile['end']['sum_sent']['lost_packets']
        self.sent_packets           = jsonfile['end']['sum_sent']['packets']
        #self.sent_sender            = jsonfile['end']['sum_sent']['sender']
        
        self.received_bps           = jsonfile['end']['sum_received']['bits_per_second']
        self.received_bytes         = jsonfile['end']['sum_received']['bytes']
        self.received_jitter        = jsonfile['end']['sum_received']['jitter_ms']
        self.received_lost_packets  = jsonfile['end']['sum_received']['lost_packets']
        self.received_packets       = jsonfile['end']['sum_received']['packets']
        #self.received_sender        = jsonfile['end']['sum_received']['sender']
        
        self.cpu_host_total         = jsonfile['end']['cpu_utilization_percent']['host_total']
        self.cpu_host_system        = jsonfile['end']['cpu_utilization_percent']['host_total']
        self.cpu_remote_system      = jsonfile['end']['cpu_utilization_percent']['remote_system']
        
        self.target_bitrate         = jsonfile['start']['target_bitrate']
        self.protocol               = jsonfile['start']['test_start']['protocol']
        self.num_streams            = jsonfile['start']['test_start']['num_streams']
        self.duration               = jsonfile['start']['test_start']['duration']
        self.cookie                 = jsonfile['start']['cookie']
        self.sender                 = jsonfile['end']['sum']['sender']
    
    def print_data(self):
        print("Sent BPS          = " + "{:.3f}".format(self.sent_bps / 1000000) + " Mbits")
        print("Sent bytes        = " + str(self.sent_bytes / 10000) + " Mbytes")
        print("Retransmits       = " + str(self.retransmits))
        print("Received BPS      = " + "{:.3f}".format(self.received_bps / 1000000) + " Mbits")
        print("Received bytes    = " + str(self.received_bytes / 10000) + " Mbytes")
        print("CPU Host total    = " + "{:.2f}".format(self.cpu_host_total) + "%")
        print("CPU Host system   = " + "{:.2f}".format(self.cpu_host_system) + "%")
        print("CPU Remote system = " + "{:.2f}".format(self.cpu_remote_system) + "%")
        print("Target Bitrate    = " + str(self.target_bitrate / 1000000) + " Mbit/s")
        print("Protocol          = " + self.protocol)
        print("Parallel          = " + str(self.num_streams))
        print("Duration          = " + str(self.duration) + "s")
        print("Cookie            = " + self.cookie)

def analyze_tcp(tcp_tests: list[Iperf3DataTCP]):
    bps_target_bit_tcp_upload = []
    bps_target_bit_tcp_dwload = []
    
    retrans_target_tcp = []
    
    for t in tcp_tests:
        #if t.num_streams == 1:
        if t.is_sender:
            retrans_target_tcp.append({
                'target': t.target_bitrate / 1000000,
                'retrans': t.retransmits,
            })
            bps_target_bit_tcp_upload.append({
                'target': t.target_bitrate / 1000000,
                'actual': t.sent_bps / 1000000,
            })
        else:
            bps_target_bit_tcp_dwload.append({
                'target': t.target_bitrate / 1000000,
                'actual': t.sent_bps / 1000000,
            })
        
    
    target_vs_actual_plot(
        bps_target_bit_tcp_upload, 
        'actual_vs_target_bitrate_tcp_upload.png', 
        'TCP Upload Target Bitrate vs Actual Bitrate')
    
    target_vs_actual_plot(
        bps_target_bit_tcp_dwload, 
        'actual_vs_target_bitrate_tcp_download.png', 
        'TCP Download Target Bitrate vs Actual Bitrate')
    
    # 2) Retransmits vs target bitrate
    plt.close()
    df = pd.DataFrame(retrans_target_tcp)
    mean_df = df.groupby('target', as_index=False)['retrans'].mean()
    print("\nbps_target_bit:\n")
    mean_df.sort_values(by=['target'], inplace=True)
    print(mean_df)
    
    print("\nWithout mean:\n")
    df.sort_values(by=['target'], inplace=True)
    print(df)
    
    
    plt.plot(mean_df['target'], mean_df['retrans'], marker='o', linestyle='-')
    plt.xlabel("Target Bitrate")
    plt.ylabel("Retransmissions")
    
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig('actual_bitrate_vs_retransmissions_tcp.png')
    print("Plot saved to actual_bitreate_vs_retransmissions.png")
    
def analyze_udp(udp_tests: list[Iperf3DataUDP]):
    # 3 cases:
    #    1) Sender statistics
    #    2) Receiver statistics
    #    3) Both
    # For now we only care about 1 and 2
    
    # For now three statistics: Bitrate, Lost Packets, Jitter
    bitrate_vs_target_sender = []
    bitrate_vs_target_receiver = []
    lost_vs_target_sender = []
    lost_vs_target_receiver = []
    jitter_vs_target_sender = []
    jitter_vs_target_receiver = []
    
    # TODO: Check if the values actually correspond
    for t in udp_tests:
        if t.sender:
            bitrate_vs_target_sender.append({
                'target': t.target_bitrate / 1000000,
                'actual': t.sent_bps / 1000000,
            })
            lost_vs_target_sender.append({
                'target': t.target_bitrate / 1000000,
                'lost': t.received_lost_packets,
                'sent': t.received_packets,
            })
            jitter_vs_target_sender.append({
                'target': t.target_bitrate / 1000000,
                'jitter': t.received_jitter,
            })
        else:
            bitrate_vs_target_receiver.append({
                'target': t.target_bitrate / 1000000,
                'actual': t.received_bps / 1000000,
            })
            lost_vs_target_receiver.append({
                'target': t.target_bitrate / 1000000,
                'lost': t.sent_lost_packets,
                'sent': t.sent_packets,
            })
            jitter_vs_target_receiver.append({
                'target': t.target_bitrate / 1000000,
                'jitter': t.sent_jitter,
            })
    
    target_vs_actual_plot(
        bitrate_vs_target_sender, 
        'actual_vs_target_bitrate_udp_upload.png', 
        'UDP Upload Target Bitrate vs Actual Bitrate')
    
    target_vs_actual_plot(
        bitrate_vs_target_receiver, 
        'actual_vs_target_bitrate_udp_download.png', 
        'UDP Download Target Bitrate vs Actual Bitrate')
    
    jitter_plot(jitter_vs_target_sender, 
                "jitter_vs_target_bitrate_udp_upload.png",
                'Jitter (ms) vs Target Bitrate Upload')
    
    jitter_plot(jitter_vs_target_receiver, 
                "jitter_vs_target_bitrate_udp_download.png",
                'Jitter (ms) vs Target Bitrate Download')
    
    lost_packet_plot(lost_vs_target_sender, 
                "lost_pck_vs_target_bitrate_udp_upload.png",
                'Lost Packets vs Target Bitrate Upload')
    
    lost_packet_plot(lost_vs_target_receiver, 
                "lost_pck_vs_target_bitrate_udp_download.png",
                'Lost Packets vs Target Bitrate Download')
 
def lost_packet_plot(data, name, title):
    df = pd.DataFrame(data)
    df.sort_values(by=['target'], inplace=True)
    mean_df = df.groupby('target', as_index=False)['lost'].mean()
    #mean_df = df.groupby('target', as_index=False)['sent'].mean()
    
    plt.plot(mean_df['target'], mean_df['lost'], linestyle='-')
    plt.xlabel("Target Bitrate")
    plt.ylabel("Lost Packets")
    plt.title(title)
    
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()
    
def target_vs_actual_plot(data, name, title):
    df = pd.DataFrame(data)
    df.sort_values(by=['target'], inplace=True)
    mean_df = df.groupby('target', as_index=False)['actual'].mean()
    
    plt.plot(mean_df['target'], mean_df['actual'], linestyle='-')
    plt.xlabel("Target Bitrate")
    plt.ylabel("Actual Bitrate")
    plt.title(title)
    
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()
    

def jitter_plot(data, name, title):
    df = pd.DataFrame(data)
    df.sort_values(by=['target'], inplace=True)
    mean_df = df.groupby('target', as_index=False)['jitter'].mean()
    
    plt.plot(mean_df['target'], mean_df['jitter'], linestyle='-')
    plt.xlabel("Target Bitrate")
    plt.ylabel("Jitter")
    plt.title(title)
    
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()
               
def main():
    directory = path.normpath('/home/estugon/Sources/bachelor_thesis/Evaluation/iperf3-tests/masq-iperf-container/iperf-logs/')
    
    onlyfiles = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    ## TEST
    testfile = "/home/estugon/Sources/bachelor_thesis/Evaluation/iperf3-tests/testparser/testinvalid.json"
    with open(testfile, 'r') as fh:
        tmpfile = fh.read()
        
    concat_data = re.sub(r"\}\n\{", "},{", tmpfile)
    json_data_as_str = f"[{concat_data}]"
    jsontest = json.loads(json_data_as_str)
    print(jsontest)
    
    client = jsontest[0]
    server = jsontest[1]
    
    print(client)
    print(server)
    
    return
    udp_tests = []
    tcp_tests = []
    tests = []
    for f in onlyfiles:
        p = join(directory, f)
        with open(p, 'r') as fh:
            file = fh.read()
        jsondata = json.loads(file)
        if 'error' not in jsondata:
            if "UDP" in f: 
                t = Iperf3DataUDP()
                t.parse(jsondata)
                udp_tests.append(t)
            elif "TCP" in f:
                t = Iperf3DataTCP()
                t.parse(jsondata)
                tcp_tests.append(t)       
        else:
            print("Failed test: " + p)

    analyze_udp(udp_tests)
    analyze_tcp(tcp_tests)
    ##for t in tests:
    ##    t.print_data()
    ##    print("----------------------------------------")
    #
    ## Planned graphs:
    #
    ## 1) BPS vs target bitrate 
    #bps_target_bit_tcp = []
    #
    #retrans_target_tcp = []
    #
    #for t in tcp_tests:
    #    #if t.num_streams == 1:
    #    bps_target_bit_tcp.append({
    #        'target': t.target_bitrate / 1000000,
    #        'bps': t.sent_bps / 1000000,
    #    })
    #    retrans_target_tcp.append({
    #        'target': t.target_bitrate / 1000000,
    #        'retrans': t.retransmits,
    #    })
    #
    #df = pd.DataFrame(bps_target_bit_tcp)
    #df.sort_values(by=['target'], inplace=True)
    #mean_df = df.groupby('target', as_index=False)['bps'].mean()
    #print("\nbps_target_bit:")
    #print(mean_df)
    #
    #plt.plot(mean_df['target'], mean_df['bps'], marker='o', linestyle='-')
    #plt.xlabel("Target Bitrate")
    #plt.ylabel("Actual Bitrate")
    #
    #plt.grid(True)
    #plt.tight_layout()
#
    ## Save the plot to a file
    #plt.savefig('actual_vs_target_bitrate.png')
    #print("Plot saved to actual_vs_target_bitrate.png")
    #
    ## 2) Retransmits vs target bitrate
    #plt.close()
    #df = pd.DataFrame(retrans_target_tcp)
    #mean_df = df.groupby('target', as_index=False)['retrans'].mean()
    #print("\nbps_target_bit:\n")
    #mean_df.sort_values(by=['target'], inplace=True)
    #print(mean_df)
    #
    #print("\nWithout mean:\n")
    #df.sort_values(by=['target'], inplace=True)
    #print(df)
    #
    #
    #plt.plot(mean_df['target'], mean_df['retrans'], marker='o', linestyle='-')
    #plt.xlabel("Target Bitrate")
    #plt.ylabel("Retransmissions")
    #
    #plt.grid(True)
    #plt.tight_layout()
#
    ## Save the plot to a file
    #plt.savefig('actual_bitreate_vs_retransmissions.png')
    #print("Plot saved to actual_bitreate_vs_retransmissions.png")
    #
    ## UDP TESTS
    
    
    
    
if __name__ == "__main__":
    main()