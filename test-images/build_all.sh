#!/bin/bash

echo "Building iperf3 image!"
docker buildx build --tag iperf3_client ./iperf3-docker/

echo "Building Masquerade Client image!"
docker buildx build --tag masq_iperf3_client ./masquerade-client/ --network=host

echo "Building Masquerade Server image!"
docker build -t masq_server ./masquerade-server-docker/ --network=host