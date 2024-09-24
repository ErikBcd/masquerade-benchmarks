#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-DOWNLOAD-DELAY-$TESTCASE-$time.json"

tc qdisc replace dev eth0 root netem loss 0.0%

# Setup ingress traffic (aka: Set download traffic to be affected by tc limitations)
tc qdisc add dev eth0 handle ffff: ingress

tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0

# TCP DOWNLOAD test with regularly changing delay

echo "TCP Download test with changing delay | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" --set-mss $PACKET_SIZE -O 2 --reverse --get-server-output --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev ifb0 root netem delay 10ms
sleep 10

tc qdisc replace dev ifb0 root netem delay 20ms
sleep 10

tc qdisc replace dev ifb0 root netem delay 50ms
sleep 10

tc qdisc replace dev ifb0 root netem delay 20ms
sleep 10

tc qdisc replace dev ifb0 root netem delay 10ms
sleep 10

tc qdisc replace dev ifb0 root netem delay 0ms

wait
