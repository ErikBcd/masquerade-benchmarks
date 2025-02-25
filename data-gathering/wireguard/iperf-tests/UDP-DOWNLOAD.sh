#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T$TESTTIME-UDP-DOWNLOAD-PACKET_SIZE-$PACKET_SIZE-$TESTCASE-$time.json"

iperf3 -c $IPERF_SERVER_IP -p 7070 -u -t "$TESTTIME" -b "$BITRATE"M -P "$PARALLEL" --reverse -l $PACKET_SIZE --get-server-output -O 2 --json --logfile "$json_path"