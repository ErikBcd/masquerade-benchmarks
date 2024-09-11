#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-UPLOAD-DELAY-$TESTCASE-$time.json"

# TCP UPLOAD test with regularly changing delay

echo "TCP Upload test with changing delay | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev eth0 root netem delay 10ms
sleep 10

tc qdisc replace dev eth0 root netem delay 20ms
sleep 10

tc qdisc replace dev eth0 root netem delay 50ms
sleep 10

tc qdisc replace dev eth0 root netem delay 20ms
sleep 10

tc qdisc replace dev eth0 root netem delay 10ms
sleep 10

tc qdisc replace dev eth0 root netem delay 0ms

wait
