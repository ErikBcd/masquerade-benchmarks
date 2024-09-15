import json
import math
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt

def main():
    masq_dir = path.normpath(
        "../raw-test-results/60s-1000mbits-50mbitInterval-masquerade/"
    )
    wg_dir = path.normpath(
        "../raw-test-results/60s-1000mbits-50mbitInterval-WireGuard/"
    )

    masq_results = [f for f in os.listdir(masq_dir) if isfile(join(masq_dir, f))]
    wg_results = [f for f in os.listdir(wg_dir) if isfile(join(wg_dir, f))]

    udp_tests_masq = []
    tcp_tests_masq = []
    for f in masq_results:
        p = join(masq_dir, f)
        with open(p, "r") as fh:
            file = fh.read()

        jsondata = json.loads(file)
        #print("Parsing: " + p)
        if "error" not in jsondata:
            if "UDP" in f:
                t = Iperf3DataUDP()
                t.parse(jsondata)
                udp_tests_masq.append(t)
            elif "TCP" in f:
                t = Iperf3DataTCP()
                t.parse(jsondata)
                tcp_tests_masq.append(t)
        else:
            print("Failed test: " + p)

    udp_tests_wg = []
    tcp_tests_wg = []
    for f in wg_results:
        p = join(wg_dir, f)
        with open(p, "r") as fh:
            file = fh.read()

        jsondata = json.loads(file)
        #print("Parsing: " + p)
        if "error" not in jsondata:
            if "UDP" in f:
                t = Iperf3DataUDP()
                t.parse(jsondata)
                udp_tests_wg.append(t)
            elif "TCP" in f:
                t = Iperf3DataTCP()
                t.parse(jsondata)
                tcp_tests_wg.append(t)
        else:
            print("Failed test: " + p)
    analyze_tcp(tcp_tests_masq, tcp_tests_wg, '../test-result-graphs/joined_results/reliable_1000mbits_60s/tcp/')

def analyze_tcp(tcp_tests_masq: list[Iperf3DataTCP], tcp_tests_wg: list[Iperf3DataTCP], base_path):
    bps_upload_wg = []
    bps_upload_masq = []
    bps_dwload_wg = []
    bps_dwload_masq = []

    retrans_upload_wg = []
    retrans_upload_masq = []
    retrans_dwload_wg = []
    retrans_dwload_masq = []

    rtt_upload_wg = []
    rtt_upload_masq = []
    rtt_dwload_wg = []
    rtt_dwload_masq = []

    for t in tcp_tests_wg:
        if t.is_upload:
            retrans_upload_wg.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_upload_wg.append({
                "target": t.target_bps / 1000000,
                "actual": t.bps / 1000000,
                "received": t.bps_received / 1000000,
            })
            rtt_upload_wg.append({
                "target": t.target_bps / 1000000,
                "max_rtt": t.max_rtt * 0.001,
                "min_rtt": t.min_rtt * 0.001,
                "mean_rtt": t.mean_rtt * 0.001, 
            })
        else:
            retrans_dwload_wg.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_dwload_wg.append({
                "target": t.target_bps / 1000000,
                "actual": t.bps / 1000000,
                "received": t.bps_received / 1000000,
            })
            rtt_dwload_wg.append({
                "target": t.target_bps / 1000000,
                "max_rtt": t.max_rtt * 0.001,
                "min_rtt": t.min_rtt * 0.001,
                "mean_rtt": t.mean_rtt * 0.001, 
            })

    for t in tcp_tests_masq:
        if t.is_upload:
            retrans_upload_masq.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_upload_masq.append({
                "target": t.target_bps / 1000000,
                "actual": t.bps / 1000000,
                "received": t.bps_received / 1000000,
            })
            rtt_upload_masq.append({
                "target": t.target_bps / 1000000,
                "max_rtt": t.max_rtt * 0.001,
                "min_rtt": t.min_rtt * 0.001,
                "mean_rtt": t.mean_rtt * 0.001, 
            })
        else:
            retrans_dwload_masq.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_dwload_masq.append({
                "target": t.target_bps / 1000000,
                "actual": t.bps / 1000000,
                "received": t.bps_received / 1000000,
            })
            rtt_dwload_masq.append({
                "target": t.target_bps / 1000000,
                "max_rtt": t.max_rtt * 0.001,
                "min_rtt": t.min_rtt * 0.001,
                "mean_rtt": t.mean_rtt * 0.001, 
            })
    
    retransmit_plot(
        retrans_upload_wg,
        retrans_upload_masq,
        base_path + "retransmits_vs_bitrate_tcp_upload",
        "TCP Upload Target Bitrate vs Retransmitted Packets",
    )

    retransmit_plot(
        retrans_dwload_wg,
        retrans_dwload_masq,
        base_path + "retransmits_vs_bitrate_tcp_download",
        "TCP Download Target Bitrate vs Retransmitted Packets",
    )

    target_vs_actual_plot(
        bps_upload_wg,
        bps_upload_masq,
        base_path + "bps_vs_target_tcp_upload",
        "TCP Upload Target Bitrate vs Measured Bitrate"
    )

    target_vs_actual_plot(
        bps_dwload_wg,
        bps_dwload_masq,
        base_path + "bps_vs_target_tcp_download",
        "TCP Download Target Bitrate vs Measured Bitrate"
    )
    
    bps_over_time(
        100, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)
    
    bps_over_time(
        200, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)
    
    bps_over_time(
        900, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)
    
    bps_over_time(
        1000, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)

def retransmit_plot(data_wg, data_masq, path, title):
    plt.close()
    df_wg = pd.DataFrame(data_wg)
    mean_df_wg = df_wg.groupby("target", as_index=False)["retrans"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("target", as_index=False)["retrans"].mean()

    plt.plot(mean_df_masq["target"], mean_df_masq["retrans"], linestyle="-", label = "Masquerade", color = 'b')
    plt.plot(mean_df_wg["target"], mean_df_wg["retrans"], linestyle="-", label = "WireGuard", color = 'r')
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Retransmissions")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".svg")
    plt.close()

def target_vs_actual_plot(data_wg, data_masq, name, title):
    plt.close()
    df_wg = pd.DataFrame(data_wg)
    df_wg.sort_values(by=["target"], inplace=True)
    mean_df_wg = df_wg.groupby("target", as_index=False)["actual"].mean()
    df_masq = pd.DataFrame(data_masq)
    df_masq.sort_values(by=["target"], inplace=True)
    mean_df_masq = df_masq.groupby("target", as_index=False)["actual"].mean()

    plt.plot(mean_df_wg["target"], mean_df_wg["actual"], linestyle="-", label = "WireGuard", color = 'r')
    plt.plot(mean_df_masq["target"], mean_df_masq["actual"], linestyle="-", label = "Masquerade", color = 'b')
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Actual Bitrate (Mbit/s)")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".svg")
    plt.close()

# Shows how the bps developed over time
def bps_over_time(target_bps, tcp_tests_masq: list[Iperf3DataTCP], tcp_tests_wg: list[Iperf3DataTCP], base_path):
    # First create dataframe which will contain timestamps and bps measurements    
    bps_download_masq = []
    bps_upload_masq = []
    
    for t in tcp_tests_masq: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                for s in t.server_streams:
                    if s.omitted or math.trunc(s.seconds) != 1:
                        continue
                    bps_upload_masq.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps / 1000000
                    })
            else:
                for s in t.client_streams: # Download tests: Client measures bps
                    if s.omitted or math.trunc(s.seconds) != 1:
                        continue
                    bps_download_masq.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps / 1000000
                    })
                    
    bps_download_wg = []
    bps_upload_wg = []
    
    for t in tcp_tests_wg: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                for s in t.server_streams:
                    if s.omitted or math.trunc(s.seconds) != 1:
                        continue
                    bps_upload_wg.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps / 1000000
                    })
            else:
                for s in t.client_streams: # Download tests: Client measures bps
                    if s.omitted or math.trunc(s.seconds) != 1:
                        continue
                    bps_download_wg.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps / 1000000
                    })
    bps_over_time_plt(
        bps_download_wg, 
        bps_download_masq, 
        base_path + "bps_over_time_download_" + str(target_bps) + "mbits_target",
        "TCP Download bitrate over time | Target bitrate: " + str(target_bps) + "mbit/s",
        target_bps,
        [0, 10, 20, 30, 40, 50, 60],
        [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0],
        2.0,
        "Fake Packet Loss (%)",
        "Fake Packet Loss"
    )
    
def bps_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title, 
    target, 
    condition_time, 
    condition_val, 
    max_cond_val,
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["bps"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["bps"].mean()
    
    ax = plt.gca()
    ax.set_ylim([0.0, target + 10])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, target + 10])

    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["bps"], linestyle="-", label = "Masquerade", color = 'b')
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["bps"], linestyle="-", label = "WireGuard", color = 'r')
    
    ax2 = ax1.twinx()
    ax2.set_ylim([0.0, max_cond_val])
    ax2.step(condition_time, condition_val, where='post', label=cond_legend, color='orange', linestyle='-', marker='o')
    ax2.set_ylabel(cond_axis_title, color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower center')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Bitrate (mbit/s)")
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".svg")
    plt.close()

if __name__ == "__main__":
    main()