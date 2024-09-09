#!/bin/bash
#echo "Testcase=$1"
#time="$(date -u +%Y-%m-%dT%H_%M_%S)"
#json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-TCP-UPLOAD-$TESTCASE-$time.json"
#
#iperf3 -c $IPERF_SERVER_IP --port 7070 -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path"

# Start in server mode on port 7070, show results as json, exit after one test
iperf3 -s --port 7070 --json --one-off