#!/bin/sh

# Ensure the /dev/net/tun device exists
if [ ! -c /dev/net/tun ]; then
    mkdir -p /dev/net
    mknod /dev/net/tun c 10 200
    chmod 600 /dev/net/tun
fi

cp -n ./client_config.toml /config/client_config.toml

time="$(date -u +%Y-%m-%dT%H_%M_%S)"
client_log="/config/client-logs/$time.log"
mkdir /config/client-logs/
# Run the Rust program with the detected network interface name

echo ""
echo ""

echo "#################################################################"
echo "######################xxx---IP ROUTE---xxx#######################"
echo "#################################################################"
ip route del default
ip route add default via 10.9.0.1
ip route add 172.20.0.200 via 172.20.0.1 dev eth0 proto dhcp src 172.20.0.100 metric 100

echo ""
echo ""

echo "#################################################################"
echo "################xxx---SETTING IPTABLE RULES---xxx################"
echo "#################################################################"
#iptables -A OUTPUT -p udp --dport 7070 -j ACCEPT
#iptables -A OUTPUT -p udp --sport 7070 -j ACCEPT
#iptables -A INPUT -p udp --dport 7070 -j ACCEPT
#iptables -A INPUT -p udp --sport 7070 -j ACCEPT
#iptables -A FORWARD -p udp --dport 7070 -j ACCEPT
#iptables -A FORWARD -p udp --sport 7070 -j ACCEPT
#iptables -A OUTPUT -p tcp --sport 7070 -j ACCEPT
#iptables -A OUTPUT -p tcp --dport 7070 -j ACCEPT
#iptables -A INPUT -p tcp --sport 7070 -j ACCEPT
#iptables -A INPUT -p tcp --dport 7070 -j ACCEPT
#iptables -A FORWARD -p tcp --sport 7070 -j ACCEPT
#iptables -A FORWARD -p tcp --dport 7070 -j ACCEPT

iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
sudo iptables -A INPUT -p udp --dport 7070 -d 0/0 -s 0/0 -j ACCEPT
sudo iptables -A INPUT -p udp --sport 7070 -d 0/0 -s 0/0 -j ACCEPT

echo ""
echo ""

echo "#################################################################"
echo "###################xxx---IP ROUTE SHOW---xxx#####################"
echo "#################################################################"
ip a
echo "#################################################################"
ip route show
echo "#################################################################"

echo ""
echo ""
# Wait a little till the server is up and running
sleep 2s

echo "#################################################################"
echo "####################xxx---iperf3 START---xxx#####################"
echo "#################################################################"

RUST_LOG=error /usr/local/bin/connect_ip_client