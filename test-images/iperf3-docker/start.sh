#!/bin/bash

modprobe ifb
ip link add ifb0 type ifb
ip link set dev ifb0 up

# Wait a little till the client is running
sleep 3s

exec /tests/$CURRENT.sh 

echo "Test done!"