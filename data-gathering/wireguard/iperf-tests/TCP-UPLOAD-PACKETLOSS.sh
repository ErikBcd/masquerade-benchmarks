#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-TCP-UPLOAD-$TESTCASE-$time.json"

# TCP UPLOAD test with regularly changing packetloss

iperf3 -c $IPERF_SERVER_IP --port 7070 -t 60 -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.0%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.0%

wait
