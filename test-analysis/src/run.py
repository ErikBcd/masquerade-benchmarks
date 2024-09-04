import json
from os import path
import os
from os.path import isfile, join

from testparser import Iperf3DataTCP, Iperf3DataUDP

import pandas as pd
import matplotlib.pyplot as plt


def analyze_tcp(tcp_tests: list[Iperf3DataTCP]):
    bps_target_bit_tcp_upload = []
    bps_target_bit_tcp_dwload = []

    retrans_target_tcp_upload = []
    retrans_target_tcp_download = []
    
    rtt_target_upload   = []
    rtt_target_download = []

    for t in tcp_tests:
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
        "../test-result-graphs/actual_vs_target_bitrate_tcp_upload.png",
        "TCP Upload Target Bitrate vs Actual Bitrate",
    )

    target_vs_actual_plot(
        bps_target_bit_tcp_dwload,
        "../test-result-graphs/actual_vs_target_bitrate_tcp_download.png",
        "TCP Download Target Bitrate vs Actual Bitrate",
    )
    retransmit_plot(
        retrans_target_tcp_upload,
        "../test-result-graphs/retransmits_vs_bitrate_tcp_upload.png",
        "TCP Upload Target Bitrate vs Retransmitted Packets",
    )
    retransmit_plot(
        retrans_target_tcp_download,
        "../test-result-graphs/retransmits_vs_bitrate_tcp_download.png",
        "TCP Download Target Bitrate vs Retransmitted Packets",
    )
    rtt_vs_target(
        rtt_target_upload,
        "../test-result-graphs/mean_rtt_vs_target_tcp_upload.png",
        "TCP Upload RTT vs Target Bitrate"
    )
    rtt_vs_target(
        rtt_target_download,
        "../test-result-graphs/mean_rtt_vs_target_tcp_download.png",
        "TCP Download RTT vs Target Bitrate"
    )


def analyze_udp(udp_tests: list[Iperf3DataUDP]):
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
        "../test-result-graphs/actual_vs_target_bitrate_udp_upload.png",
        "UDP Upload Target Bitrate vs Actual Bitrate",
    )

    target_vs_actual_plot(
        bitrate_vs_target_download,
        "../test-result-graphs/actual_vs_target_bitrate_udp_download.png",
        "UDP Download Target Bitrate vs Actual Bitrate",
    )

    jitter_plot(
        jitter_vs_target_upload,
        "../test-result-graphs/jitter_vs_target_bitrate_udp_upload.png",
        "Jitter (ms) vs Target Bitrate Upload",
    )

    jitter_plot(
        jitter_vs_target_download,
        "../test-result-graphs/jitter_vs_target_bitrate_udp_download.png",
        "Jitter (ms) vs Target Bitrate Download",
    )

    lost_packet_plot(
        lost_vs_target_upload,
        "../test-result-graphs/lost_pck_vs_target_bitrate_udp_upload.png",
        "Lost Packets vs Target Bitrate Upload",
    )

    lost_packet_plot(
        lost_vs_target_download,
        "../test-result-graphs/lost_pck_vs_target_bitrate_udp_download.png",
        "Lost Packets vs Target Bitrate Download",
    )


def lost_packet_plot(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)
    mean_df = df.groupby("target", as_index=False)["lost"].mean()
    # mean_df = df.groupby('target', as_index=False)['sent'].mean()

    plt.plot(mean_df["target"], mean_df["lost"], linestyle="-")
    plt.xlabel("Target Bitrate (Mbit/s)")
    plt.ylabel("Lost Packets")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
    plt.close()


def rtt_vs_target(data, name, title):
    plt.close()
    df = pd.DataFrame(data)
    df.sort_values(by=["target"], inplace=True)
    mean_df = df.groupby("target", as_index=False)["mean_rtt"].mean()

    plt.plot(mean_df["target"], mean_df["mean_rtt"], linestyle="-")
    plt.xlabel("Target Bitrate (Mbit/s)")
    # TODO: Check how the RTT is measured
    plt.ylabel("Mean RTT (ms)")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(name)
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
        "/home/estugon/Sources/bachelor_thesis/Evaluation/masquerade-benchmarks/raw-test-results/15s-1100mbits-masquerade"
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

    analyze_udp(udp_tests)
    analyze_tcp(tcp_tests)


if __name__ == "__main__":
    main()
