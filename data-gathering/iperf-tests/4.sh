#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-UDP-DOWNLOAD-$TESTCASE-$time.json"

iperf3 -c 192.168.0.45 -p 7070 --bind 10.9.0.2 -u -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" --reverse --get-server-output -O 2 --json --logfile "$json_path"