#!/bin/bash

docker buildx build --tag masq_iperf3_client_external . --network=host 