import json
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt

wireguard_color = 'red'
masquerade_color = 'blue'
condition_color = 'green'
condition_line_style = ':'

def main():
    masq_dir = path.normpath(
        "../raw-test-results/unreliability_tests/masquerade-70s-200mbits-50/"
    )
    wg_dir = path.normpath(
        "../raw-test-results/unreliability_tests/wireguard-70s-200mbits-50/"
    )

    masq_results = [f for f in os.listdir(masq_dir) if isfile(join(masq_dir, f))]
    wg_results = [f for f in os.listdir(wg_dir) if isfile(join(wg_dir, f))]

    udp_tests_masq_pl = []
    udp_tests_masq_bandwidth = []
    udp_tests_masq_delay = []
    tcp_tests_masq_pl = []
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
                    tcp_tests_masq_pl.append(t)
                elif "BANDWIDTH" in f:
                    tcp_tests_masq_bandwidth.append(t)
                elif "DELAY" in f:
                    tcp_tests_masq_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
        else:
            print("Failed test: " + p)

    udp_tests_wg_pl = []
    udp_tests_wg_bandwidth = []
    udp_tests_wg_delay = []
    tcp_tests_wg_pl = []
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
                    tcp_tests_wg_pl.append(t)
                elif "BANDWIDTH" in f:
                    tcp_tests_wg_bandwidth.append(t)
                elif "DELAY" in f:
                    tcp_tests_wg_delay.append(t)
                else:
                    print("UNKNOWN TESTTYPE")
        else:
            print("Failed test: " + p)
    
    analyze_tcp(
        tcp_tests_masq_pl, 
        tcp_tests_wg_pl, 
        '../test-result-graphs/joined_results/unreliable_1000mbits_70s/tcp/packetloss/',
        [0, 10, 20, 30, 40, 50, 60, 70],
        [0.0, 0.5, 1.0, 1.5, 1.0, 0.5, 0.0, 0.0],
        "packetloss",
        "Packet Loss (%)",
        "Packet Loss")
    
    analyze_tcp(
        tcp_tests_masq_delay, 
        tcp_tests_wg_delay, 
        '../test-result-graphs/joined_results/unreliable_1000mbits_70s/tcp/delay/',
        [0, 10, 20, 30, 40, 50, 60, 70],
        [0, 10, 20, 50, 20, 10, 0, 0],
        "delay",
        "Latency (ms)",
        "Latency")
    
    analyze_tcp(
        tcp_tests_masq_bandwidth, 
        tcp_tests_wg_bandwidth, 
        '../test-result-graphs/joined_results/unreliable_1000mbits_70s/tcp/bandwidth/',
        [10, 20, 30, 40, 50, 60],
        [50, 30, 10, 30, 50, 50],
        "bandwidth",
        "Bandwidth Limit (mbit/s)",
        "Bandwidth Limit")

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
        "TCP Upload Target Bitrate vs Retransmitted Packets with " + condition_legend_label,
    )

    retransmit_plot(
        retrans_dwload_wg,
        retrans_dwload_masq,
        base_path + "retransmits_vs_bitrate_tcp_download_" + condition_name,
        "TCP Download Target Bitrate vs Retransmitted Packets with " + condition_legend_label,
    )

    target_vs_actual_plot(
        bps_upload_wg,
        bps_upload_masq,
        base_path + "bps_vs_target_tcp_upload_" + condition_name,
        "TCP Upload Target Bitrate vs Measured Bitrate with " + condition_legend_label,
    )

    target_vs_actual_plot(
        bps_dwload_wg,
        bps_dwload_masq,
        base_path + "bps_vs_target_tcp_download_" + condition_name,
        "TCP Download Target Bitrate vs Measured Bitrate with " + condition_legend_label,
    )
    
    interval_plots(
        50, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    interval_plots(
        100, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    interval_plots(
        150, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)
    
    interval_plots(
        200, 
        tcp_tests_masq, 
        tcp_tests_wg, 
        base_path,
        condition_times,
        condition_values,
        condition_name,
        condition_axis_label,
        condition_legend_label)

def retransmit_plot(data_wg, data_masq, path, title):
    plt.close()
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
    plt.savefig(path + ".svg")
    plt.close()

def target_vs_actual_plot(data_wg, data_masq, name, title):
    plt.close()
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
    plt.savefig(name + ".svg")
    plt.close()

# Shows how the bps developed over time
def interval_plots(
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
            if not t.is_upload:
                i = 0
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
                        "timestamp": i,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
            else:
                i = 0
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
    
    for t in tcp_tests_wg: # Download tests: Server measures bps (not 100% sure!)
        if t.target_bps == target_bps * 1000000:
            if not t.is_upload:
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
                        "timestamp": i,
                        "rtt": s.rtt * 0.001,
                    })
                    i += 1
    
    bps_over_time_plt(
        bps_download_wg, 
        bps_download_masq, 
        base_path + "bps_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Download bitrate over time | Target bitrate: " + str(target_bps) + "mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    bps_over_time_plt(
        bps_upload_wg, 
        bps_upload_masq, 
        base_path + "bps_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Upload bitrate over time | Target bitrate: " + str(target_bps) + "mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    rtt_over_time_plt(
        rtt_download_wg, 
        rtt_download_masq, 
        base_path + "rtt_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Download RTT over time | Target bitrate: " + str(target_bps) + "mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    rtt_over_time_plt(
        rtt_upload_wg, 
        rtt_upload_masq, 
        base_path + "rtt_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Upload RTT over time | Target bitrate: " + str(target_bps) + "mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    retransmits_over_time_plt(
        retrans_upload_wg, 
        retrans_upload_masq, 
        base_path + "retrans_over_time_upload_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Upload Retransmits over time at " + str(target_bps) + "mbit/s | " + condition_legend_label,
        condition_times,
        condition_values,
        condition_axis_label,
        condition_legend_label
    )
    
    retransmits_over_time_plt(
        retrans_download_wg, 
        retrans_download_masq, 
        base_path + "retrans_over_time_download_" + str(target_bps) + "mbits_target_" + condition_name,
        "TCP Download Retransmits over time at " + str(target_bps) + "mbit/s | " + condition_legend_label,
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
        ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style)
        ax2.set_ylabel(cond_axis_title, color=condition_color)
        ax2.tick_params(axis='y', labelcolor=condition_color)
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax2.fill_between(condition_time, condition_val, step='post', alpha=0.4)
    else:
        ax1.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style)
        ax1.fill_between(condition_time, condition_val, step='post', alpha=0.4)
        
    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["rtt"], linestyle="-", label = "Masquerade", color = masquerade_color)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["rtt"], linestyle="-", label = "WireGuard", color = wireguard_color)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Latency" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper center')
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
    plt.savefig(path + ".svg")
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

    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["bps"], linestyle="-", label = "Masquerade", color = masquerade_color)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["bps"], linestyle="-", label = "WireGuard", color = wireguard_color)
    if "Bandwidth" not in cond_legend:
        ax2 = ax1.twinx()
        ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
        ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style)
        ax2.set_ylabel(cond_axis_title, color=condition_color)
        ax2.tick_params(axis='y', labelcolor=condition_color)
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax2.fill_between(condition_time, condition_val, step='post', alpha=0.4)
    else:
        ax1.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style)
        ax1.fill_between(condition_time, condition_val, step='post', alpha=0.4)
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Bandwidth" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper center')
    elif "Latency" in cond_legend:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')
    else:
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

    ax1.plot(mean_df_masq["timestamp"], mean_df_masq["retransmits"], linestyle="-", label = "Masquerade", color = masquerade_color)
    ax1.plot(mean_df_wg["timestamp"], mean_df_wg["retransmits"], linestyle="-", label = "WireGuard", color = wireguard_color)

    ax2 = ax1.twinx()
    ax2.set_ylim([0.0, (max(condition_val) + (max(condition_val) * 0.5))])
    ax2.step(condition_time, condition_val, where='post', label=cond_legend, color=condition_color, linestyle=condition_line_style)
    ax2.set_ylabel(cond_axis_title, color=condition_color)
    ax2.tick_params(axis='y', labelcolor=condition_color)
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.fill_between(condition_time, condition_val, step='post', alpha=0.4)
    
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    
    if "Bandwidth" in cond_legend:
        ax1.legend(lines_1, labels_1, loc='upper center')
    elif "Latency" in cond_legend:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')
    else:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower center')
    
    ax1.set_xlabel("Timestamp (s)")
    ax1.set_ylabel("Retransmitted Packets")
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