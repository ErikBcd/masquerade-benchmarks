#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-UDP-UPLOAD-PACKETLOSS-$TESTCASE-PACKET_SIZE-$PACKET_SIZE-$time.json"

echo "UDP Upload test with changing packet loss | Bitrate: $BITRATE"

# UDP UPLOAD test with regularly changing delay

iperf3 -c $IPERF_SERVER_IP --port 7070 -u -t 70 -b "$BITRATE"M -P "$PARALLEL" -l $PACKET_SIZE -O 2 --get-server-output --json --logfile "$json_path" &

sleep 12

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.0%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 1.0%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.5%
sleep 10

tc qdisc replace dev eth0 root netem loss 0.0%

wait
