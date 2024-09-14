#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-UDP-DOWNLOAD-PACKETLOSS-$TESTCASE-$time.json"

echo "UDP Download test with changing packet loss | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP -p 7070 -u -t 70 -b "$BITRATE"M -P "$PARALLEL" --reverse --get-server-output -O 2 --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.0%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.0%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.0%

wait