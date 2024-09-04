#!/bin/bash

START=1
TESTS=3
TEST_TIME=15 # 15s + 2s ommited 
PARALLEL=1

docker compose down --remove-orphans

# Run tests with different bitrates in succession

# TCP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in {10..1100..10}
    do
        echo "Testing $i M ($x / $TESTS)"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e CURRENT=1 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for TCP UPLOAD"
done

# UDP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in {10..1100..10}
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e CURRENT=2 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for UDP UPLOAD"
done

# TCP DOWNLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in {10..1100..10}
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e CURRENT=3 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for TCP DOWNLOAD"
done

# UDP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in {10..1100..10}
    do
        echo "Testing $i M"
        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="$x" -e CURRENT=4 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for UDP DOWNLOAD"
done
