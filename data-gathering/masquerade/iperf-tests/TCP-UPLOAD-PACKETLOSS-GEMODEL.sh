#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-T$TESTTIME-TCP-UPLOAD-PACKETLOSS-GEMODEL-$TESTCASE-PACKET_SIZE-$PACKET_SIZE-$time.json"
tc qdisc replace dev eth0 root netem loss 0.0%
tc qdisc replace dev ifb0 root netem loss 0.0%
#sleep infinity

# TCP UPLOAD test with regularly changing packetloss

echo "TCP Upload test with changing packet loss | Bitrate: $BITRATE"

iperf3 -c $IPERF_SERVER_IP --port 7070 -t "$TESTTIME" -b "$BITRATE"M -O 2 --get-server-output --json --logfile "$json_path" --set-mss $PACKET_SIZE &

# Sleep till omitted tests are over
sleep 2

# Packet loss according to Gilbert-Elliot
# 1% probability of going into a lossy state, 10% probability of leaving that state
# 70% packet loss during lossy state, 0.1% loss during good state
tc qdisc replace dev eth0 root netem loss gemodel 1% 10% 70% 0.1%

wait
