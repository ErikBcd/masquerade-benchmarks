#!/bin/sh

echo "#################################################################"
echo "###########xxx--- SETTING NETWORK UNRELIABILITY---xxx############"
echo "#################################################################"

#tc qdisc replace dev eth0 root netem loss "$PACKETLOSS_PERCENTAGE"%
tc qdisc replace dev eth0 root netem delay 100ms 20ms distribution normal

echo ""
echo ""

sleep infinity