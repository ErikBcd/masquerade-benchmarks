#!/bin/bash

####-----------------------------------####
#           TEST CONFIGURATION            #
####-----------------------------------####

# Define the number of tests ran per bitrate
START=1
TESTS=5

# iPerf3 parameters
SERVER_IP="192.168.0.45"
TEST_TIME=60 
PARALLEL=1

# Define the bitrate intervals
# Tests will start at BITRATE_START, and then the 
# bitrate will be incremented by BITRATE_STEP for each test till
# it reaches BITRATE_END
BITRATE_START=50
BITRATE_STEP=50
BITRATE_END=1000

# Make sure none of the containers are still active (cleanup)
docker compose down --remove-orphans

# Print the approximate duration for all tests
let "num_tests=($BITRATE_END / $BITRATE_STEP) * $TESTS * 4"
let "seconds=$num_tests * ($TEST_TIME + 5)"
let "in_hours=($seconds / 60) / 60"

echo "Running $num_tests tests, will be done in ${in_hours}h"

####-----------------------------------####
#             TEST EXECUTION              #
####-----------------------------------####

## Run $TESTS tests for each type of {TCP Upload, TCP Download, UDP Upload, UDP Download}
## for each of the defined bitrates



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

## For long tests it's nice to automatically shut the system down afterwards
## Uncomment this if you want that

#echo "TESTS DONE! SHUTTING DOWN IN 5 MINUTES!"
#sleep 300

#shutdown now

####-----------------------------------####
#             TEST EXAMPLES               #
####-----------------------------------####

# Here are some examples for individual tests
# Useful if you want to test one specific test, or if you want to first do a testrun with all tests 
# to check whether they all work

# TCP UPLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-DELAY" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-BANDWIDTH" iperf3
#docker-compose down --remove-orphans
#
## TCP DOWNLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-PACKETLOSS" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-DELAY" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-BANDWIDTH" iperf3
#docker-compose down --remove-orphans
#
## UDP UPLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-DELAY" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-BANDWIDTH" iperf3
#docker-compose down --remove-orphans
#
## UDP DOWNLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-PACKETLOSS" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-DELAY" iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-BANDWIDTH" iperf3
#docker-compose down --remove-orphans