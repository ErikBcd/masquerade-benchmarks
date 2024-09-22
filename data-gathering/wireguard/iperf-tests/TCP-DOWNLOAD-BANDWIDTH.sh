#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-DOWNLOAD-BANDWIDTH-$TESTCASE-$time.json"

# Setup ingress traffic (aka: Set download traffic to be affected by tc limitations)
tc qdisc add dev eth0 handle ffff: ingress

tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
tc qdisc replace dev ifb0 root netem loss 0.0%

# TCP DOWNLOAD test with regularly changing bandwidth

echo "TCP Download test with changing bandwidth | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" -O 2 --set-mss $PACKET_SIZE --reverse --get-server-output --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev ifb0 root tbf rate 50mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev ifb0 root tbf rate 30mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev ifb0 root tbf rate 10mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev ifb0 root tbf rate 30mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev ifb0 root tbf rate 50mbit burst 32kbit latency 400ms
sleep 10

#tc qdisc del dev ifb0 root
tc qdisc replace dev ifb0 root tbf rate 1000mbit burst 32kbit latency 400ms


wait
