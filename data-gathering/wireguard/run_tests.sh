#!/bin/bash

START=1
TESTS=5
TEST_TIME=15
PARALLEL=1

BITRATE_START=20
BITRATE_STEP=20
BITRATE_END=1000

SERVER_IP="192.168.0.45"

docker compose down --remove-orphans

let "num_tests=($BITRATE_END / $BITRATE_STEP) * $TESTS * 4"
let "seconds=$num_tests * ($TEST_TIME + 5)"
let "in_hours=($seconds / 60) / 60"

echo "Running $num_tests tests, will be done in ${in_hours}h"

# Run tests with different bitrates in succession

# TCP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M ($x / $TESTS)"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT=1 iperf3
        docker-compose down --remove-orphans
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
    done
    echo "Done ($x / $TESTS) for UDP DOWNLOAD"
done

echo "TESTS DONE! SHUTTING DOWN IN 5 MINUTES!"
sleep 300

shutdown now