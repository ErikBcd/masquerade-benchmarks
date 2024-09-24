import json
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt

# Graph look & feel options
wireguard_color = '#e02214'
wireguard_area_color = '#eba09b'
masquerade_color = '#1e14e0'
masquerade_area_color = '#9d9bcf'
linewidth = 4.0
condition_color = 'green'
condition_fill_color = 'green'
condition_fill_alpha = 0.2
condition_line_style = ':'

fontsize=30
figuresize=(13,9)
figuresize_wider=(15,9)

# Testfile directories
masq_dir = path.normpath(
        "../raw-test-results/unreliability_tests/masquerade-70s-200mbits-50-mtu/"
)
wg_dir = path.normpath(
    "../raw-test-results/unreliability_tests/wireguard-70s-200mbits-mtu/"
)
# Output for the plots
output_path = "../test-result-graphs/joined_results/unreliable_1000mbits_70s/limited-mtu/"

def main():
    masq_results = [f for f in os.listdir(masq_dir) if isfile(join(masq_dir, f))]
    wg_results = [f for f in os.listdir(wg_dir) if isfile(join(wg_dir, f))]

    udp_tests_masq_pl_mtu200 = []
    udp_tests_masq_pl = []
    udp_tests_masq_bandwidth = []
    udp_tests_masq_delay = []
    tcp_tests_masq_pl = []
    tcp_tests_masq_pl_mtu200 = []
    tcp_tests_masq_bandwidth = []
    tcp_tests_masq_delay = []
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
                if "PACKETLOSS" in f:
                    if "PACKET_SIZE-200" in f:
                        udp_tests_masq_pl_mtu200.append(t)
                    else:
                        udp_tests_masq_pl.append(t)
                elif "BANDWIDTH" in f:
                    udp_tests_masq_bandwidth.append(t)
                elif "DELAY" in f:
                    udp_tests_masq_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
            elif "TCP" in f:
                t = Iperf3DataTCP()
                t.parse(jsondata)
                if "PACKETLOSS" in f:
                    if "PACKET_SIZE-200" in f:
                        tcp_tests_masq_pl_mtu200.append(t)
                    else:
                        tcp_tests_masq_pl.append(t)
                    #tcp_tests_masq_pl.append(t)
                elif "BANDWIDTH" in f:
                    tcp_tests_masq_bandwidth.append(t)
                elif "DELAY" in f:
                    tcp_tests_masq_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
        else:
            print("Failed test: " + p)

    udp_tests_wg_pl_mtu200 = []
    udp_tests_wg_pl = []
    udp_tests_wg_bandwidth = []
    udp_tests_wg_delay = []
    tcp_tests_wg_pl = []
    tcp_tests_wg_pl_mtu200 = []
    tcp_tests_wg_bandwidth = []
    tcp_tests_wg_delay = []
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
                if "PACKETLOSS" in f:
                    if "PACKET_SIZE-200" in f:
                        udp_tests_wg_pl_mtu200.append(t)
                    else:
                        udp_tests_wg_pl.append(t)
                elif "BANDWIDTH" in f:
                    udp_tests_wg_bandwidth.append(t)
                elif "DELAY" in f:
                    udp_tests_wg_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
            elif "TCP" in f:
                t = Iperf3DataTCP()
                t.parse(jsondata)
                if "PACKETLOSS" in f:
                    if "PACKET_SIZE-200" in f:
                        tcp_tests_wg_pl_mtu200.append(t)
                    else:
                        tcp_tests_wg_pl.append(t)
                elif "BANDWIDTH" in f:
                    tcp_tests_wg_bandwidth.append(t)
                elif "DELAY" in f:
                    tcp_tests_wg_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
        else:
            print("Failed test: " + p)
    
    if len(tcp_tests_masq_pl_mtu200) != 0:
        analyze_tcp(
            tcp_tests_masq_pl_mtu200, 
            tcp_tests_wg_pl_mtu200, 
            output_path + '/tcp/packetloss/mtu200_',
            [0, 10, 20, 30, 40, 50, 60, 70],
            [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0, 0.0],
            "packetloss",
            "Packet Loss (%)",
            "Packet Loss")
    
    analyze_tcp(
        tcp_tests_masq_pl, 
        tcp_tests_wg_pl, 
        output_path + '/tcp/packetloss/',
        [0, 10, 20, 30, 40, 50, 60, 70],
        [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0, 0.0],
        "packetloss",
        "Packet Loss (%)",
        "Packet Loss")
    
    analyze_tcp(
        tcp_tests_masq_delay, 
        tcp_tests_wg_delay, 
        output_path + '/tcp/delay/',
        [0, 10, 20, 30, 40, 50, 60, 70],
        [0, 10, 20, 50, 20, 10, 0, 0],
        "delay",
        "Latency (ms)",
        "Latency")
    
    analyze_tcp(
        tcp_tests_masq_bandwidth, 
        tcp_tests_wg_bandwidth, 
        output_path + '/tcp/bandwidth/',
        [10, 20, 30, 40, 50, 60],
        [50, 30, 10, 30, 50, 50],
        "bandwidth",
        "Bandwidth Limit (Mbit/s)",
        "Bandwidth")
    
    # TODO: Fix packet loss results
    #if len(udp_tests_masq_pl) != 0:
    #    analyze_udp(
    #        udp_tests_masq_pl, 
    #        udp_tests_wg_pl, 
    #        '../test-result-graphs/joined_results/unreliable_1000mbits_70s/udp/packetloss/',
    #        [0, 10, 20, 30, 40, 50, 60, 70],
    #        [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0, 0.0],
    #        "packetloss",
    #        "Packet Loss (%)",
    #        "Packet Loss")
    #else:
    #    print("No usable udp tests for packet loss at mtu 800!")
    
    if len(udp_tests_masq_pl_mtu200) != 0:
        analyze_udp(
            udp_tests_masq_pl_mtu200, 
            udp_tests_wg_pl_mtu200, 
            output_path + '/udp/packetloss/mtu200_',
            [0, 10, 20, 30, 40, 50, 60, 70],
            [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0, 0.0],
            "packetloss",
            "Packet Loss (%)",
            "Packet Loss")
    
    analyze_udp(
        udp_tests_masq_delay, 
        udp_tests_wg_delay, 
        output_path + '/udp/delay/',
        [0, 10, 20, 30, 40, 50, 60, 70],
        [0, 10, 20, 50, 20, 10, 0, 0],
        "delay",
        "Latency (ms)",
        "Latency")
    
    analyze_udp(
        udp_tests_masq_bandwidth, 
        udp_tests_wg_bandwidth, 
        output_path + '/udp/bandwidth/',
        [10, 20, 30, 40, 50, 60],
        [50, 30, 10, 30, 50, 50],
        "bandwidth",
        "Bandwidth Limit (Mbit/s)",
        "Bandwidth")

def analyze_tcp(
    tcp_tests_masq: list[Iperf3DataTCP], 
    tcp_tests_wg: list[Iperf3DataTCP], 
    base_path,
    condition_times,
    condition_values,
    condition_name,
    condition_axis_label,
    condition_legend_label):
    
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
        base_path + "retransmits_vs_bitrate_tcp_upload_" + condition_name,
        "TCP Upload Target Bitrate vs Retransmitted Packets \n" + condition_legend_label,
    )

    retransmit_plot(
        retrans_dwload_wg,
        retrans_dwload_masq,
        base_path + "retransmits_vs_bitrate_tcp_download_" + condition_name,
        "TCP Download Target Bitrate vs Retransmitted Packets \n" + condition_legend_label,
    )

    target_vs_actual_plot(
        bps_upload_wg,
        bps_upload_masq,
        base_path + "bps_vs_target_tcp_upload_" + condition_name,
        "TCP Upload Target Bitrate vs Measured Bitrate \n" + condition_legend_label,
    )

    target_vs_actual_plot(
        bps_dwload_wg,
        bps_dwload_masq,
        base_path + "bps_vs_target_tcp_download_" + condition_name,
        "TCP Download Target Bitrate vs Measured Bitrate \n" + condition_legend_label,
    )
    
    tcp_interval_plots(
        50, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    tcp_interval_plots(
        100, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    tcp_interval_plots(
        150, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    tcp_interval_plots(
        200, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)

def analyze_udp(
    udp_tests_masq: list[Iperf3DataUDP], 
    udp_tests_wg: list[Iperf3DataUDP], 
    base_path,
    condition_times,
    condition_values,
    condition_name,
    condition_axis_label,
    condition_legend_label):
    masq_bitrate_vs_target_upload = []
    masq_bitrate_vs_target_download = []
    masq_lost_vs_target_upload = []
    
    masq_jitter_vs_target_upload = []
    masq_jitter_vs_target_download = []
    
    wg_bitrate_vs_target_upload = []
    wg_bitrate_vs_target_download = []
    wg_lost_vs_target_upload = []
    
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
             
    lost_packet_plot(
        wg_lost_vs_target_upload,
        masq_lost_vs_target_upload,
        base_path + "lost_pck_vs_target_bitrate_udp_upload_" + condition_name,
        "UDP Upload Lost Packets \n" + condition_legend_label
    )
    
    jitter_plot(
        wg_jitter_vs_target_upload,
        masq_jitter_vs_target_upload,
        base_path + "jitter_vs_target_bitrate_udp_upload_" + condition_name,
        "Jitter (ms) vs Target Bitrate Upload \n" + condition_legend_label
    )
    
    jitter_plot(
        wg_jitter_vs_target_download,
        masq_jitter_vs_target_download,
        base_path + "jitter_vs_target_bitrate_udp_download_" + condition_name,
        "Jitter (ms) vs Target Bitrate Download \n" + condition_legend_label
    )
    
    target_vs_actual_plot(
        wg_bitrate_vs_target_upload,
        masq_bitrate_vs_target_upload,
        base_path + "bps_vs_target_udp_upload_" + condition_name,
        "UDP Upload Target Bitrate vs Measured Bitrate \n" + condition_legend_label
    )

    target_vs_actual_plot(
        wg_bitrate_vs_target_download,
        masq_bitrate_vs_target_download,
        base_path + "bps_vs_target_udp_download_" + condition_name,
        "UDP Download Target Bitrate vs Measured Bitrate \n" + condition_legend_label
    )
    
    udp_interval_plots(
        50, 
        udp_tests_masq, 
        udp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    udp_interval_plots(
        100, 
        udp_tests_masq, 
        udp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    udp_interval_plots(
        150, 
        udp_tests_masq, 
        udp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    udp_interval_plots(
        200, 
        udp_tests_masq, 
        udp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)

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
    
    plt.errorbar(agg_df_wg['target'], agg_df_wg['mean_lost'], yerr=agg_df_wg['std_lost'], fmt='o-', capsize=5, label='WireGuard')
    plt.errorbar(agg_df_masq['target'], agg_df_masq['mean_lost'], yerr=agg_df_masq['std_lost'], fmt='o-', capsize=5, label='Masquerade')
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean ± Std) vs Target Bitrate | ' + title)
    plt.legend()
    plt.savefig(name + "_errorbar.png", dpi=300)
    plt.savefig(name + "_errorbar.pdf")
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    
    # Shaded area plot for lost packets (min-max range)
    plt.plot(agg_df_wg['target'], agg_df_wg['mean_lost'], marker='o', label='WireGuard')
    plt.plot(agg_df_masq['target'], agg_df_masq['mean_lost'], marker='o', label='Masquerade')
    plt.fill_between(agg_df_wg['target'], agg_df_wg['min_lost'], agg_df_wg['max_lost'], color=wireguard_area_color, alpha=0.3, label='Min-Max Range WireGuard')
    plt.fill_between(agg_df_masq['target'], agg_df_masq['min_lost'], agg_df_masq['max_lost'], color=masquerade_area_color, alpha=0.3, label='Min-Max Range Masquerade')
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean with Min-Max Range) vs Target Bitrate | ' + title)
    plt.legend()
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
    
    df_masq = pd.DataFrame(masq_data)
    df_masq.sort_values(by=["target"], inplace=True)
    mean_df_masq = df_masq.groupby("target", as_index=False)["jitter"].mean()

    plt.plot(mean_df_wg["target"], mean_df_wg["jitter"], linestyle="-", label="WireGuard", linewidth=linewidth)
    plt.plot(mean_df_masq["target"], mean_df_masq["jitter"], linestyle="-", label="Masquerade", linewidth=linewidth)

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
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("target", as_index=False)["retrans"].mean()

    plt.plot(mean_df_masq["target"], mean_df_masq["retrans"], linestyle="-", label = "Masquerade", color = masquerade_color)
    plt.plot(mean_df_wg["target"], mean_df_wg["retrans"], linestyle="-", label = "WireGuard", color = wireguard_color)
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

    plt.plot(mean_df_wg["target"], mean_df_wg["received"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)
    plt.plot(mean_df_masq["target"], mean_df_masq["received"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Actual Bitrate (Mbit/s)")
    plt.title(title)

    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".pdf")
    plt.close()

def udp_interval_plots(
    target_bps, 
    udp_tests_masq: list[Iperf3DataUDP], 
    udp_tests_wg: list[Iperf3DataUDP], 
    base_path,
    condition_times,
    condition_values,
    condition_name,
    condition_axis_label,
    condition_legend_label
):
    bps_download_masq   = []
    bps_upload_masq     = []
    jitter_download_masq = []
    jitter_upload_masq = []
    packetloss_download_masq = []
    packetloss_upload_masq = []

    for t in udp_tests_masq: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                i = 2
                for s in t.intervals:
                    bps_upload_masq.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    jitter_upload_masq.append({
                        "timestamp": i,
                        "jitter": s.jitter_ms,
                    })
                    packetloss_upload_masq.append({
                        "timestamp": i,
                        "lost_packets": s.lost_packets,
                        "lost_percent": s.lost_percent
                    })
                    i += 1
            else:
                i = 2
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_masq.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    jitter_download_masq.append({
                        "timestamp": i,
                        "jitter": s.jitter_ms,
                    })
                    packetloss_download_masq.append({
                        "timestamp": i,
                        "lost_packets": s.lost_packets,
                        "lost_percent": s.lost_percent
                    })
                    i += 1
                    
    bps_download_wg   = []
    bps_upload_wg     = []
    jitter_download_wg = []
    jitter_upload_wg = []
    packetloss_download_wg = []
    packetloss_upload_wg = []

    for t in udp_tests_wg: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                i = 2
                for s in t.intervals:
                    bps_upload_wg.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    jitter_upload_wg.append({
                        "timestamp": i,
                        "jitter": s.jitter_ms,
                    })
                    packetloss_upload_wg.append({
                        "timestamp": i,
                        "lost_packets": s.lost_packets,
                        "lost_percent": s.lost_percent
                    })
                    i += 1
            else:
                i = 2
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_wg.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    jitter_download_wg.append({
                        "timestamp": i,
                        "jitter": s.jitter_ms,
                    })
                    packetloss_download_wg.append({
                        "timestamp": i,
                        "lost_packets": s.lost_packets,
                        "lost_percent": s.lost_percent
                    })
                    i += 1
                    
    bps_over_time_plt(
        bps_download_wg, 
        bps_download_masq, 
        base_path + "bps_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nUDP Download Bitrate over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    bps_over_time_plt(
        bps_upload_wg, 
        bps_upload_masq, 
        base_path + "bps_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nUDP Upload Bitrate over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    jitter_over_time_plt(
        jitter_download_wg, 
        jitter_download_masq, 
        base_path + "jitter_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nUDP Download Jitter over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    jitter_over_time_plt(
        jitter_upload_wg, 
        jitter_upload_masq, 
        base_path + "jitter_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nUDP Upload Jitter over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    packetloss_over_time_plt(
        packetloss_download_wg, 
        packetloss_download_masq, 
        base_path + "pl_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nUDP Download Packetloss over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    packetloss_over_time_plt(
        packetloss_upload_wg, 
        packetloss_upload_masq, 
        base_path + "pl_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        "UDP Upload Packetloss over time with target " + str(target_bps) + "Mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
# Shows how the bps developed over time
def tcp_interval_plots(
    target_bps, 
    tcp_tests_masq: list[Iperf3DataTCP], 
    tcp_tests_wg: list[Iperf3DataTCP], 
    base_path,
    condition_times,
    condition_values,
    condition_name,
    condition_axis_label,
    condition_legend_label):
    # First create dataframe which will contain timestamps and bps measurements    
    bps_download_masq   = []
    bps_upload_masq     = []
    
    retrans_download_masq   = []
    retrans_upload_masq     = []
    
    rtt_download_masq   = []
    rtt_upload_masq     = []
    
    for t in tcp_tests_masq: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                i = 2
                for s in t.intervals:
                    bps_upload_masq.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    retrans_upload_masq.append({
                        "timestamp": i,
                        "retransmits": s.retransmits,
                    })
                    rtt_upload_masq.append({
                        "timestamp": i+1,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
            else:
                i = 2
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_masq.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    retrans_download_masq.append({
                        "timestamp": i,
                        "retransmits": s.retransmits,
                    })
                    rtt_download_masq.append({
                        "timestamp": i,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
                    
    bps_download_wg = []
    bps_upload_wg = []
    retrans_download_wg = []
    retrans_upload_wg = []
    rtt_upload_wg = []
    rtt_download_wg = []
    
    for t in tcp_tests_wg: 
        if t.target_bps == target_bps * 1000000:
            if t.is_upload:
                i = 2
                for s in t.intervals:
                    bps_upload_wg.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    retrans_upload_wg.append({
                        "timestamp": i,
                        "retransmits": s.retransmits,
                    })
                    rtt_upload_wg.append({
                        "timestamp": i,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
            else:
                i = 2
                for s in t.intervals: # Download tests: Client measures bps
                    bps_download_wg.append({
                        "timestamp": i,
                        "bps": s.bps_received / 1000000
                    })
                    retrans_download_wg.append({
                        "timestamp": i,
                        "retransmits": s.retransmits,
                    })
                    rtt_download_wg.append({
                        "timestamp": i+1,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
    
    bps_over_time_plt(
        bps_download_wg, 
        bps_download_masq, 
        base_path + "bps_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label + "\nTCP Download bitrate over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s ",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    bps_over_time_plt(
        bps_upload_wg, 
        bps_upload_masq, 
        base_path + "bps_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label + "\nTCP Upload bitrate over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    rtt_over_time_plt(
        rtt_download_wg, 
        rtt_download_masq, 
        base_path + "rtt_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nTCP Download RTT over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    rtt_over_time_plt(
        rtt_upload_wg, 
        rtt_upload_masq, 
        base_path + "rtt_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nTCP Upload RTT over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    retransmits_over_time_plt(
        retrans_upload_wg, 
        retrans_upload_masq, 
        base_path + "retrans_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nTCP Upload Retransmits over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    retransmits_over_time_plt(
        retrans_download_wg, 
        retrans_download_masq, 
        base_path + "retrans_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        condition_legend_label+"\nTCP Download Retransmits over 70s\nTarget Bitrate: " + str(target_bps) + "Mbit/s",
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
 
def rtt_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title,
    condition_time, 
    condition_val, 
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["rtt"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["rtt"].mean()
    if mean_df_masq['rtt'].max() > mean_df_wg['rtt'].max():
        max_rtt = mean_df_masq['rtt'].max()
    else:
        max_rtt = mean_df_wg['rtt'].max()
        
    #print("Masquerade data:\n" + df_masq.to_string())
    
    ax = plt.gca()
    ax.set_ylim([0.0, max_rtt + 10])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, max_rtt + 10])

    
    if "Latency" not in cond_legend:
        ax2 = ax1.twinx()
        ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
        ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
        ax2.set_ylabel(cond_axis_title, color=condition_color)
        ax2.tick_params(axis='y', labelcolor=condition_color)
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax2.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    else:
        ax1.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
        ax1.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
        
    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["rtt"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["rtt"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Latency" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper right')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Round Trip Time (ms)")
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")
    plt.close() 

def packetloss_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title,
    condition_time, 
    condition_val, 
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["lost_percent"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["lost_percent"].mean()
    if mean_df_masq['lost_percent'].max() > mean_df_wg['lost_percent'].max():
        max_lost_percent = mean_df_masq['lost_percent'].max()
    else:
        max_lost_percent = mean_df_wg['lost_percent'].max()
        
    #print("Masquerade data:\n" + df_masq.to_string())
    
    ax = plt.gca()
    ax.set_ylim([0.0, max_lost_percent + (max_lost_percent * 0.5)])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, max_lost_percent + (max_lost_percent * 0.5)])

    
    ax2 = ax1.twinx()
    ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
    ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
    ax2.set_ylabel(cond_axis_title, color=condition_color)
    ax2.tick_params(axis='y', labelcolor=condition_color)
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    
    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["lost_percent"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["lost_percent"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Latency" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='center right')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Packetloss (%)")
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")
    plt.close() 

def jitter_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title,
    condition_time, 
    condition_val, 
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["jitter"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["jitter"].mean()
    if mean_df_masq['jitter'].max() > mean_df_wg['jitter'].max():
        max_lost_jitter = mean_df_masq['jitter'].max()
    else:
        max_lost_jitter = mean_df_wg['jitter'].max()
        
    #print("Masquerade data:\n" + df_masq.to_string())
    
    ax = plt.gca()
    ax.set_ylim([0.0, max_lost_jitter + (max_lost_jitter * 0.5)])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, max_lost_jitter + (max_lost_jitter * 0.5)])

    
    #if "Latency" not in cond_legend:
    ax2 = ax1.twinx()
    ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
    ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
    ax2.set_ylabel(cond_axis_title, color=condition_color)
    ax2.tick_params(axis='y', labelcolor=condition_color)
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    #else:
    #    ax1.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
    #    ax1.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
        
    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["jitter"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["jitter"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Latency" in cond_legend:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Jitter (ms)")
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")  

    plt.close() 

def bps_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title,
    condition_time, 
    condition_val, 
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["bps"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["bps"].mean()
    if mean_df_masq['bps'].max() > mean_df_wg['bps'].max():
        max_bps = mean_df_masq['bps'].max()
    else:
        max_bps = mean_df_wg['bps'].max()
        
    #print("Masquerade data:\n" + df_masq.to_string())
    
    ax = plt.gca()
    ax.set_ylim([0.0, max_bps + 10])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, max_bps + 10])

    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["bps"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["bps"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)
    if "Bandwidth" not in cond_legend:
        ax2 = ax1.twinx()
        ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
        ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
        ax2.set_ylabel(cond_axis_title, color=condition_color)
        ax2.tick_params(axis='y', labelcolor=condition_color)
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax2.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    else:
        ax1.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
        ax1.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Bandwidth" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper center')
    elif "Latency" in cond_legend:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower left')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Bitrate (Mbit/s)")
    plt.title(title)

    #plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    print("Saving plot as " + path + ".png")
    plt.savefig(path + ".png", dpi=300)
    plt.savefig(path + ".pdf")
    plt.close()
    
def retransmits_over_time_plt(
    data_wg, 
    data_masq, 
    path, 
    title,
    condition_time, 
    condition_val, 
    cond_axis_title, 
    cond_legend):
    
    plt.close()
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figuresize
    df_wg = pd.DataFrame(data_wg)
    
    #print("wg data: \n" + df_wg)
    mean_df_wg = df_wg.groupby("timestamp", as_index=False)["retransmits"].mean()
    df_masq = pd.DataFrame(data_masq)
    mean_df_masq = df_masq.groupby("timestamp", as_index=False)["retransmits"].mean()
    if mean_df_masq['retransmits'].max() > mean_df_wg['retransmits'].max():
        max_retransmits = mean_df_masq['retransmits'].max()
    else:
        max_retransmits = mean_df_wg['retransmits'].max()
        
    #print("Masquerade data:\n" + df_masq.to_string())
    
    ax = plt.gca()
    ax.set_ylim([0.0, max_retransmits + ((max_retransmits+2)/2)])
    
    fig, ax1 = plt.subplots()
    
    ax1.set_ylim([0.0, max_retransmits + ((max_retransmits+2)/2)])

    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["retransmits"], linestyle="-", label = "Masquerade", color = masquerade_color, linewidth=linewidth)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["retransmits"], linestyle="-", label = "WireGuard", color = wireguard_color, linewidth=linewidth)

    ax2 = ax1.twinx()
    ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
    ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style, linewidth=linewidth)
    ax2.set_ylabel(cond_axis_title, color=condition_color)
    ax2.tick_params(axis='y', labelcolor=condition_color)
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.fill_between(condition_time, condition_val, step='post', alpha=condition_fill_alpha, color=condition_fill_color)
    
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Bandwidth" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper center')
    elif "Latency" in cond_legend:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Retransmitted Packets")
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