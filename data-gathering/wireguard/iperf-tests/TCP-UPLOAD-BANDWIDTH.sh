#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-UPLOAD-BANDWIDTH-$TESTCASE-$time.json"

# TCP UPLOAD test with regularly changing bandwidth

echo "TCP Upload test with changing bandwidth | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" -O 2 --set-mss $PACKET_SIZE --get-server-output --json --logfile "$json_path" &

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

#tc qdisc del dev eth0 root
tc qdisc replace dev eth0 root tbf rate 1000mbit burst 32kbit latency 400ms

wait
