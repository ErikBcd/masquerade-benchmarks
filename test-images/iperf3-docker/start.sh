#!/bin/bash

# Wait a little till the client is running
sleep 3s

exec /tests/$CURRENT.sh 

echo "Test done!"