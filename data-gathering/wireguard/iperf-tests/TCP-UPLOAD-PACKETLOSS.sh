#!/bin/bash
#echo "Testcase=$1"
time="$(date -u +%Y-%m-%dT%H_%M_%S)"
json_path="/iperf/$BITRATE-P$PARALLEL-T70s-TCP-UPLOAD-PACKETLOSS-$TESTCASE-PACKET_SIZE-$PACKET_SIZE-$time.json"

tc qdisc replace dev eth0 root netem loss 0.0%
#sleep infinity

# TCP UPLOAD test with regularly changing packetloss

echo "TCP Upload test with changing packet loss | Bitrate: $BITRATE"

#iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" --get-server-output --json --logfile "$json_path" --set-mss $PACKET_SIZE &
iperf3 -c $IPERF_SERVER_IP --port 7070 -t 70 -b "$BITRATE"M -P "$PARALLEL" -O 2 --get-server-output --json --logfile "$json_path" --set-mss $PACKET_SIZE &

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
