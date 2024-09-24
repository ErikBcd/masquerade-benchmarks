#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-T$TESTTIME-TCP-UPLOAD-PACKETLOSS-REORDER-$TESTCASE-PACKET_SIZE-$PACKET_SIZE-$time.json"

# Fix weird qdisc/tc/netem behaviour
tc qdisc replace dev eth0 root netem loss 0.0%
tc qdisc replace dev ifb0 root netem loss 0.0%


echo "TCP Upload test with changing packet loss | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t "$TESTTIME" -b "$BITRATE"M -O 2 --get-server-output --json --logfile "$json_path" --set-mss $PACKET_SIZE &

# Sleep till omitted tests are over
sleep 2

# 5% chance to delay packets, and sends every 5th packet immediately
# This will cause packets to be in the wrong order, especially interesting for TCP
tc qdisc change dev eth0 root netem gap 5 delay 10ms reorder 5%

wait
