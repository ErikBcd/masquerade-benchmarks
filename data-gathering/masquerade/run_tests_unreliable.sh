#!/bin/bash

####-----------------------------------####
#           TEST CONFIGURATION            #
####-----------------------------------####

# Define the number of tests ran per bitrate
START=1
TESTS=6

# iPerf3 parameters
TEST_TIME=70 
PARALLEL=1
SERVER_IP="192.168.0.45"

# Define the bitrate intervals
# Tests will start at BITRATE_START, and then the 
# bitrate will be incremented by BITRATE_STEP for each test till
# it reaches BITRATE_END

BITRATE_START=50
BITRATE_STEP=50
BITRATE_END=200

# Make sure none of the containers are still active (cleanup)
docker compose down --remove-orphans

# Print the approximate duration for all tests

let "num_tests=($BITRATE_END / $BITRATE_STEP) * $TESTS * 4 * 4"
let "seconds=$num_tests * ($TEST_TIME + 5)"
let "in_hours=($seconds / 60) / 60"

echo "Running $num_tests tests, will be done in ${in_hours}h"

####-----------------------------------####
#             TEST EXECUTION              #
####-----------------------------------####

## Run $TESTS tests for each type of {TCP Upload, TCP Download, UDP Upload, UDP Download}
## for each of the defined bitrates
## There are 3 specific tests for different conditions
##  * Packet loss (incrementing packet loss. Ran 2 times, for different sized iPerf3 packets)
##  * Delay (Also called latency test)
##  * Bandwidth (Limiting the maximum available bandwidth)

# TCP UPLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M ($x / $TESTS)"

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=800  iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200  iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-DELAY" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
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

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-DELAY" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
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

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for TCP DOWNLOAD"
done

# UDP DOWNLOAD
for x in $(eval echo "{$START..$TESTS}")
do
    for i in $(seq $BITRATE_START $BITRATE_STEP $BITRATE_END)
    do
        echo "Testing $i M"

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans

        docker compose run -e BITRATE="$i" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST_$x" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
        docker-compose down --remove-orphans
    done
    echo "Done ($x / $TESTS) for UDP DOWNLOAD"
done

## For long tests it's nice to automatically shut the system down afterwards
## Uncomment this if you want that

#echo "TESTS DONE! SHUTTING DOWN IN 5 MINUTES!"
#sleep 300
#
#shutdown now


####-----------------------------------####
#             TEST EXAMPLES               #
####-----------------------------------####

# Here are some examples for individual tests
# Useful if you want to test one specific test, or if you want to first do a testrun with all tests 
# to check whether they all work

# TCP UPLOAD
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans

#docker compose run -e BITRATE=200 -e TESTTIME="60" -e PARALLEL="$PARALLEL" -e TESTCASE="INTERMEDIARY" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS-GEMODEL" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans

#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-DELAY" -e PACKET_SIZE=200  iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-UPLOAD-BANDWIDTH" -e PACKET_SIZE=800  iperf3
#docker-compose down --remove-orphans

## TCP DOWNLOAD
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans

#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="TCP-DOWNLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans


# UDP UPLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_7" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
#docker-compose down --remove-orphans
#sleep 5
#docker compose run -e BITRATE=100 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_8" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
#docker-compose down --remove-orphans
#sleep 5
#docker compose run -e BITRATE=150 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST_9" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=200 iperf3
#docker-compose down --remove-orphans
#sleep 5
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-DELAY" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-UPLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans


# UDP DOWNLOAD
#docker compose run -e BITRATE=50 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="PACKETLOSS_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans

#docker compose run -e BITRATE=100 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_7" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans
#sleep 5
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_8" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans
#sleep 5
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="DELAY_TEST_9" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-DELAY" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans
#
#docker compose run -e BITRATE=200 -e TESTTIME="$TEST_TIME" -e PARALLEL="$PARALLEL" -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="$SERVER_IP" -e CURRENT="UDP-DOWNLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
#docker-compose down --remove-orphans