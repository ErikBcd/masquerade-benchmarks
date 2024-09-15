import json
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
        print("Parsing: " + p)
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
        print("Parsing: " + p)
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
def bps_over_time(target_bps, tcp_tests_masq: list[Iperf3DataTCP], tcp_tests_wg: list[Iperf3DataTCP]):
    # First create dataframe which will contain timestamps and bps measurements
    data_masq_send = []
    data_masq_recv = []
    for t in tcp_tests_masq:
        if t.target_bps == target_bps:
            for s in t.sender_intervals:
                data_masq_send.append({
                    "timestamp": s.start,
                    "bps": s.bps
                })
            for s in t.receiver_intervals:
                data_masq_recv.append({
                    "timestamp": s.start,
                    "bps": s.bps
                })
    
    data_wg_send = []
    data_wg_recv = []
    for t in tcp_tests_wg:
        if t.target_bps == target_bps:
            for s in t.sender_intervals:
                data_wg_send.append({
                    "timestamp": s.start,
                    "bps": s.bps
                })
            for s in t.receiver_intervals:
                data_wg_recv.append({
                    "timestamp": s.start,
                    "bps": s.bps
                })

if __name__ == "__main__":
    main()