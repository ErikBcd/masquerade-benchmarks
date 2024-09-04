#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-UDP-UPLOAD-$TESTCASE-$time.json"

ip route show

#iperf3 -c 192.168.0.71 -p 7070 --bind 10.9.0.1 -u -t 5 -b 50M --json --logfile "$json_path"

iperf3 -c 192.168.0.45 -p 7070 -u -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path"