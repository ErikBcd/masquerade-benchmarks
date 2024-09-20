import json
import math
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt

wireguard_color = '#e02214'
wireguard_area_color = '#eba09b'
masquerade_color = '#1e14e0'
masquerade_area_color = '#9d9bcf'

fontsize=30
figuresize=(13,9)
figuresize_wider=(15,9)

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
    analyze_udp(udp_tests_masq, udp_tests_wg, '../test-result-graphs/joined_results/reliable_1000mbits_60s/udp/')

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
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            retrans_upload_wg.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_upload_wg.append({
                "target": t.target_bps / 1000000,
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
                "received": t.bps_received / 1000000,
            })
            rtt_dwload_wg.append({
                "target": t.target_bps / 1000000,
                "max_rtt": t.max_rtt * 0.001,
                "min_rtt": t.min_rtt * 0.001,
                "mean_rtt": t.mean_rtt * 0.001, 
            })

    for t in tcp_tests_masq:
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            retrans_upload_masq.append({
                "target": t.target_bps / 1000000,
                "retrans": t.retransmits,
            })
            bps_upload_masq.append({
                "target": t.target_bps / 1000000,
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
        "TCP Upload Target Bitrate\nvs Retransmitted Packets",
    )

    retransmit_plot(
        retrans_dwload_wg,
        retrans_dwload_masq,
        base_path + "retransmits_vs_bitrate_tcp_download",
        "TCP Download Target Bitrate\nvs Retransmitted Packets",
    )

    target_vs_actual_plot(
        bps_upload_wg,
        bps_upload_masq,
        base_path + "bps_vs_target_tcp_upload",
        "TCP Upload Target Bitrate\nvs Measured Bitrate"
    )

    target_vs_actual_plot(
        bps_dwload_wg,
        bps_dwload_masq,
        base_path + "bps_vs_target_tcp_download",
        "TCP Download Target Bitrate\nvs Measured Bitrate"
    )
    
    target_vs_rtt_plot(
        rtt_upload_wg,
        rtt_upload_masq,
        base_path + "rtt_vs_target_tcp_upload",
        "TCP Upload Target Bitrate vs RTT"
    )
    
    target_vs_rtt_plot(
        rtt_dwload_wg,
        rtt_dwload_masq,
        base_path + "rtt_vs_target_tcp_download",
        "TCP Download Target Bitrate vs RTT"
    )
    
    interval_plots_time(
        100, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)
    
    interval_plots_time(
        200, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)
    
    interval_plots_time(
        900, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path)

def analyze_udp(udp_tests_masq: list[Iperf3DataUDP], udp_tests_wg: list[Iperf3DataUDP], base_path):
    masq_bitrate_vs_target_upload = []
    masq_bitrate_vs_target_download = []
    masq_lost_vs_target_upload = []
    masq_lost_vs_target_download = []
    
    masq_jitter_vs_target_upload = []
    masq_jitter_vs_target_download = []
    
    wg_bitrate_vs_target_upload = []
    wg_bitrate_vs_target_download = []
    wg_lost_vs_target_upload = []
    wg_lost_vs_target_download = []
    
    wg_jitter_vs_target_upload = []
    wg_jitter_vs_target_download = []
    
    for t in udp_tests_masq:
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            masq_bitrate_vs_target_upload.append({
                "target": t.target_bps / 1000000,
                "received": t.received_bps / 1000000,
            })
            masq_lost_vs_target_upload.append({
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "percentage": t.lost_percent,
            })
            masq_jitter_vs_target_upload.append({
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
            })
        else:
            masq_bitrate_vs_target_download.append({
                "target": t.target_bps / 1000000,
                "received": t.received_bps / 1000000,
            })
            masq_jitter_vs_target_download.append({
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
            })
            masq_lost_vs_target_download.append({
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "percentage": t.lost_percent,
            })
    for t in udp_tests_wg:
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            wg_bitrate_vs_target_upload.append({
                "target": t.target_bps / 1000000,
                "received": t.received_bps / 1000000,
            })
            wg_lost_vs_target_upload.append({
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "percentage": t.lost_percent,
            })
            wg_jitter_vs_target_upload.append({
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
            })
        else:
            wg_bitrate_vs_target_download.append({
                "target": t.target_bps / 1000000,
                "received": t.received_bps / 1000000,
            })
            wg_jitter_vs_target_download.append({
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
            })
            wg_lost_vs_target_download.append({
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "percentage": t.lost_percent,
            })
            
    #lost_packet_plot(
    #    wg_lost_vs_target_download,
    #    masq_lost_vs_target_download,
    #    base_path + "lost_pck_vs_target_bitrate_udp_download",
    #    "Download"
    #)

    lost_packet_plot(
        wg_lost_vs_target_upload,
        masq_lost_vs_target_upload,
        base_path + "lost_pck_vs_target_bitrate_udp_upload",
        "Upload"
    )
    
    jitter_plot(
        wg_jitter_vs_target_upload,
        masq_jitter_vs_target_upload,
        base_path + "jitter_vs_target_bitrate_udp_upload",
        "Jitter (ms) vs Target Bitrate Upload",
    )
    
    jitter_plot(
        wg_jitter_vs_target_download,
        masq_jitter_vs_target_download,
        base_path + "jitter_vs_target_bitrate_udp_download",
        "Jitter (ms) vs Target Bitrate Download",
    )
    
    target_vs_actual_plot(
        wg_bitrate_vs_target_upload,
        masq_bitrate_vs_target_upload,
        base_path + "bps_vs_target_udp_upload",
        "UDP Upload Target Bitrate\nvs Measured Bitrate"
    )

    target_vs_actual_plot(
        wg_bitrate_vs_target_download,
        masq_bitrate_vs_target_download,
        base_path + "bps_vs_target_udp_download",
        "UDP Download Target Bitrate\nvs Measured Bitrate"
    )

def lost_packet_plot(data_wg, data_masq, name, title):
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    df_masq = pd.DataFrame(data_masq)
    
    agg_df_wg = df_wg.groupby('target').agg(
        mean_lost=('lost', 'mean'),
        std_lost=('lost', 'std'),
        min_lost=('lost', 'min'),
        max_lost=('lost', 'max'),
        mean_percentage=('percentage', 'mean'),
        std_percentage=('percentage', 'std')
    ).reset_index()
    
    agg_df_masq = df_masq.groupby('target').agg(
        mean_lost=('lost', 'mean'),
        std_lost=('lost', 'std'),
        min_lost=('lost', 'min'),
        max_lost=('lost', 'max'),
        mean_percentage=('percentage', 'mean'),
        std_percentage=('percentage', 'std')
    ).reset_index()
    
    plt.errorbar(agg_df_wg['target'], agg_df_wg['mean_lost'], yerr=agg_df_wg['std_lost'], fmt='o-', capsize=5, label='WireGuard', color=wireguard_color)
    plt.errorbar(agg_df_masq['target'], agg_df_masq['mean_lost'], yerr=agg_df_masq['std_lost'], fmt='o-', capsize=5, label='Masquerade', color=masquerade_color)
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean ± Std) vs Target Bitrate | ' + title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(name + "_errorbar.png", dpi=300)
    plt.savefig(name + "_errorbar.pdf")
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    # Shaded area plot for lost packets (min-max range)
    plt.plot(agg_df_wg['target'], agg_df_wg['mean_lost'], label='WireGuard', color=wireguard_color)
    plt.plot(agg_df_masq['target'], agg_df_masq['mean_lost'], label='Masquerade', color=masquerade_color)
    plt.fill_between(agg_df_wg['target'], agg_df_wg['min_lost'], agg_df_wg['max_lost'], color=wireguard_area_color, alpha=0.3, label='Min-Max Range WireGuard')
    plt.fill_between(agg_df_masq['target'], agg_df_masq['min_lost'], agg_df_masq['max_lost'], color=masquerade_area_color, alpha=0.3, label='Min-Max Range Masquerade')
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean with Min-Max Range)\nvs Target Bitrate | ' + title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(name + "_shaded.png", dpi=300)
    plt.savefig(name + "_shaded.pdf")
    
    
    plt.close()

def jitter_plot(wg_data, masq_data, name, title):
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize

    df_wg = pd.DataFrame(wg_data)
    df_wg.sort_values(by=["target"], inplace=True)
    mean_df_wg = df_wg.groupby("target", as_index=False)["jitter"].mean()
    min_df_wg = df_wg.groupby("target", as_index=False)["jitter"].min()
    max_df_wg = df_wg.groupby("target", as_index=False)["jitter"].max()
    
    df_masq = pd.DataFrame(masq_data)
    df_masq.sort_values(by=["target"], inplace=True)
    mean_df_masq = df_masq.groupby("target", as_index=False)["jitter"].mean()
    min_df_masq = df_masq.groupby("target", as_index=False)["jitter"].min()
    max_df_masq = df_masq.groupby("target", as_index=False)["jitter"].max()

    plt.plot(mean_df_wg["target"], mean_df_wg["jitter"], linestyle="-", label="WireGuard", color=wireguard_color)
    plt.plot(mean_df_masq["target"], mean_df_masq["jitter"], linestyle="-", label="Masquerade", color=masquerade_color)
    plt.fill_between(min_df_wg['target'], min_df_wg['jitter'], max_df_wg['jitter'], color=wireguard_area_color, alpha=0.3, label='Range WireGuard')
    plt.fill_between(min_df_masq['target'], min_df_masq['jitter'], max_df_masq['jitter'], color=masquerade_area_color, alpha=0.3, label='Range WireGuard')
    
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Jitter (ms)")
    plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".pdf")
    plt.close()

def retransmit_plot(data_wg, data_masq, path, title):
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize

    df_wg = pd.DataFrame(data_wg)
    mean_df_wg = df_wg.groupby("target", as_index=False)["retrans"].mean()
    max_df_wg = df_wg.groupby("target", as_index=False)["retrans"].max()
    min_df_wg = df_wg.groupby("target", as_index=False)["retrans"].min()

    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("target", as_index=False)["retrans"].mean()
    max_df_masq = df_masq.groupby("target", as_index=False)["retrans"].max()
    min_df_masq = df_masq.groupby("target", as_index=False)["retrans"].min()

    plt.plot(mean_df_masq["target"], mean_df_masq["retrans"], linestyle="-", label = "Masquerade", color = masquerade_color)
    plt.plot(mean_df_wg["target"], mean_df_wg["retrans"], linestyle="-", label = "WireGuard", color = wireguard_color)
    plt.fill_between(max_df_wg['target'], min_df_wg['retrans'], max_df_wg['retrans'], color=wireguard_area_color, alpha=0.3, label='Min-Max Range WireGuard')
    plt.fill_between(max_df_masq['target'], min_df_masq['retrans'], max_df_masq['retrans'], color=masquerade_area_color, alpha=0.3, label='Min-Max Range Masquerade')
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Retransmissions")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")
    plt.close()

def target_vs_actual_plot(data_wg, data_masq, name, title):
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize

    df_wg = pd.DataFrame(data_wg)
    df_wg.sort_values(by=["target"], inplace=True)
    mean_df_wg = df_wg.groupby("target", as_index=False)["received"].mean()
    df_masq = pd.DataFrame(data_masq)
    df_masq.sort_values(by=["target"], inplace=True)
    mean_df_masq = df_masq.groupby("target", as_index=False)["received"].mean()

    plt.plot(mean_df_wg["target"], mean_df_wg["received"], linestyle="-", label = "WireGuard", color = wireguard_color)
    plt.plot(mean_df_masq["target"], mean_df_masq["received"], linestyle="-", label = "Masquerade", color = masquerade_color)
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Actual Bitrate (Mbit/s)")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".pdf")
    plt.close()

def target_vs_rtt_plot(data_wg, data_masq, name, title):
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize

    df_wg = pd.DataFrame(data_wg)
    df_wg.sort_values(by=["target"], inplace=True)
    mean_df_wg = df_wg.groupby("target", as_index=False)["mean_rtt"].mean()
    df_masq = pd.DataFrame(data_masq)
    df_masq.sort_values(by=["target"], inplace=True)
    mean_df_masq = df_masq.groupby("target", as_index=False)["mean_rtt"].mean()

    min_wg = df_wg.groupby("target", as_index=False)["min_rtt"].mean()
    max_wg = df_wg.groupby("target", as_index=False)["max_rtt"].mean()
    min_masq = df_masq.groupby("target", as_index=False)["min_rtt"].mean()
    max_masq = df_masq.groupby("target", as_index=False)["max_rtt"].mean()
    
    plt.plot(mean_df_wg["target"], mean_df_wg["mean_rtt"], linestyle="-", label = "WireGuard", color = wireguard_color)
    plt.plot(mean_df_masq["target"], mean_df_masq["mean_rtt"], linestyle="-", label = "Masquerade", color = masquerade_color)
    plt.fill_between(min_wg['target'], min_wg['min_rtt'], max_wg['max_rtt'], color=wireguard_area_color, alpha=0.3, label='Range WireGuard')
    plt.fill_between(min_masq['target'], min_masq['min_rtt'], max_masq['max_rtt'], color=masquerade_area_color, alpha=0.3, label='Range Masquerade')
    
    
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("RTT (ms)")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".pdf")
    plt.close()

# Shows how the bps developed over time
def interval_plots_time(target_bps, tcp_tests_masq: list[Iperf3DataTCP], tcp_tests_wg: list[Iperf3DataTCP], base_path):
    # First create dataframe which will contain timestamps and bps measurements    
    bps_download_masq = []
    bps_upload_masq = []
    
    for t in tcp_tests_masq: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                for s in t.intervals:
                    bps_upload_masq.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps_received / 1000000
                    })
            else:
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_masq.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps_received / 1000000
                    })
                    
    bps_download_wg = []
    bps_upload_wg = []
    
    for t in tcp_tests_wg: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                for s in t.intervals:
                    bps_upload_wg.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps_received / 1000000
                    })
            else:
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_wg.append({
                        "timestamp": math.trunc(s.start),
                        "bps": s.bps_received / 1000000
                    })
    
    bps_over_time_plt(
        bps_download_wg, 
        bps_download_masq, 
        base_path + "bps_over_time_download_" + str(target_bps) + "mbits_target",
        "TCP Download bitrate over time | Target bitrate: " + str(target_bps) + "mbit/s",
        target_bps,
    )
    
def bps_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title, 
    target):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize

    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["bps"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["bps"].mean()
    
    ax = plt.gca()
    ax.set_ylim([0.0, target + 10])

    plt.plot(mean_df_masq["timestamp"], mean_df_masq["bps"], linestyle="-", label = "Masquerade", color = masquerade_color)
    plt.plot(mean_df_wg["timestamp"], mean_df_wg["bps"], linestyle="-", label = "WireGuard", color = wireguard_color)
    
    plt.legend()
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")
    plt.close()

if __name__ == "__main__":
    main()