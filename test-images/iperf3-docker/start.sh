#!/bin/bash

# Wait a little till the client is running

#iptables -A OUTPUT -p udp --dport 7070 -j ACCEPT
#iptables -A OUTPUT -p udp --sport 7070 -j ACCEPT
#iptables -A OUTPUT -p tcp --sport 7070 -j ACCEPT
#iptables -A OUTPUT -p tcp --dport 7070 -j ACCEPT

#iptables -P INPUT ACCEPT
#iptables -P FORWARD ACCEPT
#iptables -P OUTPUT ACCEPT

sleep 4
#echo "Testcase a=$TESTCASE"
exec /tests/$CURRENT.sh 



##echo "Saving in $json_path, Bitrate: $BITRATE"
## Run tests with different bitrates in succession
##iperf3 -c 192.168.0.71 --port 7070 -t 1s -b 1M -P "$PARALLEL"
#
#for x in {0..1}
#do
#    for i in {100..400..100}
#    do
#        json_path="/iperf/$time-$i-$x.json"
#        echo "Saving in $json_path, Bitrate: $i"
#        iperf3 -c 192.168.0.71 --port 7070 -t "$TIME" -b "$i"M -P "$PARALLEL" --json --logfile "$json_path"
#    done
#done

echo "Test done!"