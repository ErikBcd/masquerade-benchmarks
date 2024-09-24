#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-TCP-DOWNLOAD-PACKET_SIZE-$PACKET_SIZE-$TESTCASE-$time.json"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" -O 2 --set-mss $PACKET_SIZE --reverse --get-server-output --json --logfile "$json_path"