#!/bin/bash

START=1
TESTS=5
TEST_TIME=60 
PARALLEL=1

BITRATE_START=50
BITRATE_STEP=50
BITRATE_END=1000

SERVER_IP="10.8.0.1"

docker compose down --remove-orphans

let "num_tests=($BITRATE_END / $BITRATE_STEP) * $TESTS * 4"
let "seconds=$num_tests * ($TEST_TIME + 10)"
let "in_hours=($seconds / 60) / 60"

echo "Running $num_tests tests, will be done in ${in_hours}h"

# Run tests with different bitrates in succession

# test TCP and UDP
echo "TCP TEST"

docker compose run -e BITRATE="500" -e TESTTIME="60" -e PARALLEL="1" -e TESTCASE="INITIAL_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=1 iperf3
docker-compose down --remove-orphans

sleep 5
echo "UDP TEST"
docker compose run -e BITRATE="50" -e TESTTIME="10" -e PARALLEL="1" -e TESTCASE="INITIAL_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=2 iperf3
docker-compose down --remove-orphans

# TCP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M ($x / $TESTS)"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=1 iperf3
        docker-compose down --remove-orphans
        sleep 5
    done
    echo "Done ($x / $TESTS) for TCP UPLOAD"
done

# UDP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=2 iperf3
        docker-compose down --remove-orphans
        sleep 5
    done
    echo "Done ($x / $TESTS) for UDP UPLOAD"
done

# TCP DOWNLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=3 iperf3
        docker-compose down --remove-orphans
        sleep 5
    done
    echo "Done ($x / $TESTS) for TCP DOWNLOAD"
done

# UDP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=4 iperf3
        docker-compose down --remove-orphans
        sleep 5
    done
    echo "Done ($x / $TESTS) for UDP DOWNLOAD"
done

echo "TESTS DONE! SHUTTING DOWN IN 5 MINUTES!"
sleep 300

#shutdown now