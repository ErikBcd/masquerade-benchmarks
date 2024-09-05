import json
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt


def analyze_tcp(tcp_tests: list[Iperf3DataTCP], base_path):
    bps_target_bit_tcp_upload = []
    bps_target_bit_tcp_dwload = []

    retrans_target_tcp_upload = []
    retrans_target_tcp_download = []
    
    rtt_target_upload   = []
    rtt_target_download = []

    for t in tcp_tests:
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            retrans_target_tcp_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "retrans": t.retransmits,
                }
            )
            bps_target_bit_tcp_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "actual": t.bps / 1000000,
                    "received": t.bps_received / 1000000,
                }
            )
            rtt_target_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "max_rtt": t.max_rtt * 0.001,
                    "min_rtt": t.min_rtt * 0.001,
                    "mean_rtt": t.mean_rtt * 0.001, 
                }
            )
        else:
            bps_target_bit_tcp_dwload.append(
                {
                    "target": t.target_bps / 1000000,
                    "actual": t.bps / 1000000,
                    "received": t.bps_received / 1000000,
                }
            )
            retrans_target_tcp_download.append(
                {
                    "target": t.target_bps / 1000000,
                    "retrans": t.retransmits,
                }
            )
            rtt_target_download.append(
                {
                    "target": t.target_bps / 1000000,
                    "max_rtt": t.max_rtt * 0.001,
                    "min_rtt": t.min_rtt * 0.001,
                    "mean_rtt": t.mean_rtt * 0.001, 
                }
            )

    target_vs_actual_plot(
        bps_target_bit_tcp_upload,
        base_path + "actual_vs_target_bitrate_tcp_upload.png",
        "TCP Upload Target Bitrate vs Actual Bitrate",
    )

    target_vs_actual_plot(
        bps_target_bit_tcp_dwload,
        base_path + "actual_vs_target_bitrate_tcp_download.png",
        "TCP Download Target Bitrate vs Actual Bitrate",
    )
    retransmit_plot(
        retrans_target_tcp_upload,
        base_path + "retransmits_vs_bitrate_tcp_upload.png",
        "TCP Upload Target Bitrate vs Retransmitted Packets",
    )
    retransmit_plot(
        retrans_target_tcp_download,
        base_path + "retransmits_vs_bitrate_tcp_download.png",
        "TCP Download Target Bitrate vs Retransmitted Packets",
    )
    rtt_vs_target(
        rtt_target_upload,
        base_path + "mean_rtt_vs_target_tcp_upload",
        "TCP Upload RTT vs Target Bitrate"
    )
    rtt_vs_target(
        rtt_target_download,
        base_path + "mean_rtt_vs_target_tcp_download",
        "TCP Download RTT vs Target Bitrate"
    )
    
    # experiments
    target_vs_actual_plot_mult_dots(
        bps_target_bit_tcp_dwload,
        base_path + "actual_vs_target_bitrate_tcp_download_mult.png",
        "TCP Download Target Bitrate vs Actual Bitrate All Tests",
    )
    
    target_vs_actual_plot_mult_dots(
        bps_target_bit_tcp_upload,
        base_path + "actual_vs_target_bitrate_tcp_upload_mult.png",
        "TCP Upload Target Bitrate vs Actual Bitrate All Tests",
    )


def analyze_udp(udp_tests: list[Iperf3DataUDP], base_path):
    # 3 cases:
    #    1) Sender statistics
    #    2) Receiver statistics
    #    3) Both
    # For now we only care about 1 and 2

    # For now three statistics: Bitrate, Lost Packets, Jitter
    bitrate_vs_target_upload = []
    bitrate_vs_target_download = []
    lost_vs_target_upload = []
    lost_vs_target_download = []
    jitter_vs_target_upload = []
    jitter_vs_target_download = []

    for t in udp_tests:
        # Speeds get wonky above 950mbit/s because of my 1gbit network, so exclude them
        if (t.target_bps / 1000000) >= 950:
            continue
        if t.is_upload:
            bitrate_vs_target_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "actual": t.bps / 1000000,
                }
            )
            lost_vs_target_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "sent": t.packets,
                    "percentage": t.lost_percent,
                }
            )
            jitter_vs_target_upload.append(
                {
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
                }
            )
        else:
            bitrate_vs_target_download.append(
                {
                    "target": t.target_bps / 1000000,
                    "actual": t.bps / 1000000,
                }
            )
            lost_vs_target_download.append(
                {
                    "target": t.target_bps / 1000000,
                    "lost": t.lost_packets,
                    "sent": t.packets,
                    "percentage": t.lost_percent,
                }
            )
            jitter_vs_target_download.append(
                {
                    "target": t.target_bps / 1000000,
                    "jitter": t.jitter_ms,
                }
            )

    target_vs_actual_plot(
        bitrate_vs_target_upload,
        base_path + "actual_vs_target_bitrate_udp_upload.png",
        "UDP Upload Target Bitrate vs Actual Bitrate",
    )

    target_vs_actual_plot(
        bitrate_vs_target_download,
        base_path + "actual_vs_target_bitrate_udp_download.png",
        "UDP Download Target Bitrate vs Actual Bitrate",
    )

    jitter_plot(
        jitter_vs_target_upload,
        base_path + "jitter_vs_target_bitrate_udp_upload.png",
        "Jitter (ms) vs Target Bitrate Upload",
    )

    jitter_plot(
        jitter_vs_target_download,
        base_path + "jitter_vs_target_bitrate_udp_download.png",
        "Jitter (ms) vs Target Bitrate Download",
    )

    lost_packet_plot(
        lost_vs_target_upload,
        base_path + "lost_pck_vs_target_bitrate_udp_upload",
        "Upload",
    )

    lost_packet_plot(
        lost_vs_target_download,
        base_path + "lost_pck_vs_target_bitrate_udp_download",
        "Download",
    )


def lost_packet_plot(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    #df.sort_values(by=["target"], inplace=True)
    #mean_df = df.groupby("target", as_index=False)["lost"].mean()
#
    #plt.plot(mean_df["target"], mean_df["lost"], linestyle="-")
    #plt.xlabel("Target Bitrate (Mbit/s)")
    #plt.ylabel("Lost Packets")
    #plt.title(title)
#
    #plt.grid(True)
    #plt.tight_layout()
#
    #plt.savefig(name)
    # Example 1: Line plot showing target vs. lost packets
    
    agg_df = df.groupby('target').agg(
        mean_lost=('lost', 'mean'),
        std_lost=('lost', 'std'),
        min_lost=('lost', 'min'),
        max_lost=('lost', 'max'),
        mean_percentage=('percentage', 'mean'),
        std_percentage=('percentage', 'std')
    ).reset_index()
    
    plt.errorbar(agg_df['target'], agg_df['mean_lost'], yerr=agg_df['std_lost'], fmt='o-', capsize=5, label='Lost Packets')
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean ± Std) vs Target Bitrate | ' + title)
    plt.legend()
    plt.savefig(name + "_errorbar.png", dpi=300)
    plt.savefig(name + "_errorbar.svg")
    
    plt.close()
    
    # Shaded area plot for lost packets (min-max range)
    plt.plot(agg_df['target'], agg_df['mean_lost'], marker='o', label='Mean Lost Packets')
    plt.fill_between(agg_df['target'], agg_df['min_lost'], agg_df['max_lost'], color='gray', alpha=0.3, label='Min-Max Range')
    plt.xlabel('Target Bitrate (Mbps)')
    plt.ylabel('Lost Packets')
    plt.title('Lost Packets (Mean with Min-Max Range) vs Target Bitrate | ' + title)
    plt.legend()
    plt.savefig(name + "_shaded.png", dpi=300)
    plt.savefig(name + "_shaded.svg")
    
    
    plt.close()


def rtt_vs_target(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)
    mean_df_mean_rtt = df.groupby("target", as_index=False)["mean_rtt"].mean()
    mean_df_max_rtt = df.groupby("target", as_index=False)["max_rtt"].mean()
    mean_df_min_rtt = df.groupby("target", as_index=False)["min_rtt"].mean()
    
    plt.plot(mean_df_mean_rtt['target'], mean_df_mean_rtt['mean_rtt'], label='Mean RTT', color='blue', marker='.')
    plt.fill_between(mean_df_min_rtt['target'], mean_df_min_rtt['min_rtt'], mean_df_max_rtt['max_rtt'], color='gray', alpha=0.3, label='Min-Max Range')

    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Mean RTT (ms)")
    plt.title(title)
    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name + ".png", dpi=300)
    plt.savefig(name + ".svg")
    plt.close()

def target_vs_actual_plot(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)
    mean_df = df.groupby("target", as_index=False)["actual"].mean()

    plt.plot(mean_df["target"], mean_df["actual"], linestyle="-")
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Actual Bitrate (Mbit/s)")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()
    
def target_vs_actual_plot_mult_dots(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)

    #plt.plot(mean_df["target"], mean_df["actual"], linestyle="-")
    plt.plot(kind="scatter", marker="o")
    plt.scatter(df["target"], df["actual"])
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Actual Bitrate (Mbit/s)")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()


def jitter_plot(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)
    mean_df = df.groupby("target", as_index=False)["jitter"].mean()

    plt.plot(mean_df["target"], mean_df["jitter"], linestyle="-")
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Jitter (ms)")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()


def retransmit_plot(data, path, title):
    plt.close()
    df = pd.DataFrame(data)
    mean_df = df.groupby("target", as_index=False)["retrans"].mean()
    # print("\nbps_target_bit:\n")
    # mean_df.sort_values(by=['target'], inplace=True)
    # print(mean_df)
    #
    # print("\nWithout mean:\n")
    # df.sort_values(by=['target'], inplace=True)
    # print(df)

    plt.plot(mean_df["target"], mean_df["retrans"], linestyle="-")
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Retransmissions")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(path)
    plt.close()


def main():
    directory = path.normpath(
        "../raw-test-results/60s-1000mbits-50mbitInterval-masquerade/"
    )

    onlyfiles = [f for f in os.listdir(directory) if isfile(join(directory, f))]

    udp_tests = []
    tcp_tests = []
    for f in onlyfiles:
        p = join(directory, f)
        with open(p, "r") as fh:
            file = fh.read()

        jsondata = json.loads(file)
        if "error" not in jsondata:
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

    analyze_udp(udp_tests, '../test-result-graphs/60s-1000mbit-50mbit/udp/')
    analyze_tcp(tcp_tests, '../test-result-graphs/60s-1000mbit-50mbit/tcp/')


if __name__ == "__main__":
    main()
