#!/bin/bash

docker buildx build --tag masq_iperf3_client . --network=host 