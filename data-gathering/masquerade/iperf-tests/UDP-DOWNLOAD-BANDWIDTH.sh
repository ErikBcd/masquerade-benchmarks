#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-UDP-DOWNLOAD-BANDWIDTH-$TESTCASE-$time.json"

echo "UDP Download test with changing bandwidth | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP -p 7070 -u -t 70 -b "$BITRATE"M -P "$PARALLEL" --reverse --get-server-output -O 2 --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev eth0 root tbf rate 50mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev eth0 root tbf rate 30mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev eth0 root tbf rate 10mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev eth0 root tbf rate 30mbit burst 32kbit latency 400ms
sleep 10

tc qdisc replace dev eth0 root tbf rate 50mbit burst 32kbit latency 400ms
sleep 10

tc qdisc del dev eth0 root

wait