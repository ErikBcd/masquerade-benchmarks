#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-TCP-UPLOAD-$TESTCASE-$time.json"

iperf3 -c 192.168.0.45 --port 7070 -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path"
