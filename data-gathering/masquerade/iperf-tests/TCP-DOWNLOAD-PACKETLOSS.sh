#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-DOWNLOAD-PACKETLOSS-$TESTCASE-PACKET_SIZE-$PACKET_SIZE-$time.json"

# Setup ingress traffic (aka: Set download traffic to be affected by tc limitations)
tc qdisc add dev eth0 handle ffff: ingress

tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0

# TCP DOWNLOAD test with regularly changing packetloss

echo "TCP Download test with changing packet loss | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" -O 2 --reverse --get-server-output --json --set-mss $PACKET_SIZE --logfile "$json_path" &

sleep 12

tc qdisc replace dev ifb0 root netem loss 0.5%
sleep 10

tc qdisc replace dev ifb0 root netem loss 1.0%
sleep 10

tc qdisc replace dev ifb0 root netem loss 1.5%
sleep 10

tc qdisc replace dev ifb0 root netem loss 1.0%
sleep 10

tc qdisc replace dev ifb0 root netem loss 0.5%
sleep 10

tc qdisc replace dev ifb0 root netem loss 0.0%

wait
