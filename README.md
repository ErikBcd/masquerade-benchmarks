# masquerade-benchmarks

Benchmarking setup for Masquerade and Wireguard.

## data-gathering
.. contains scripts for starting the containers and doing tests.

In the folder you will find test setups for both wireguard and masquerade, both are very similiar besides how the docker-compose files for the VPNs are configured.

### Running a test

#### iPerf3 Client

The Docker container for iPerf3 accepts multiple environment variables that will configure which test is run, and how its run. The following environment variables can be added:

* CURRENT [default = 1]
    * Name of the testfile that should be ran (excluding extension)
    * Testfile has to exist inside the `iperf-tests` directory in the same location where the `docker-compose.yml` file is located
    * Always required
* TESTCASE
    * Descriptor for the testcase
    * This is used for automated tests, where you can set this to the 
* IPERF_SERVER_IP
    * IP of the iPerf3 server
* TESTTIME [ Seconds ]
    * For how long the test is supposed to be ran
* BITRATE [ Mbit/s, default = 100 ]
    * How much data the iPerf3 sender is supposed to be sending in Mbit/s
* PACKET_SIZE [ bytes ]
    * The maximum size of individual packets that iPerf3 will send
* PARALLEL
    * How many tests should be ran in parallel

*Note:* All of the env vars besides CURRENT are only used by the existing test scripts, so if you create your own test scripts you can leave them out/add some as needed.

An example to start a TCP upload test with introduced packetloss:
```
docker compose run -e BITRATE=200 -e TESTTIME=60 -e PARALLEL=1 -e TESTCASE="1" -e IPERF_SERVER_IP="192.168.0.45" -e CURRENT="TCP-UPLOAD-PACKETLOSS" -e PACKET_SIZE=800 iperf3
```

In addition to that, each VPN test directory also includes test scripts for automated tests that you can change to your liking. These are called `run_tests.sh` and `run_tests_unreliable.sh`, and can be used as further examples.

The folders also contain the relevant config directories of Masquerade/WireGuard. These can be left alone, however they can also be used to change some VPN settings (e.g. for Masquerade options like the congestion algorithm, thread channel size, pacing options, qlog files, ...).
#### iPerf3 Server

The server can be ran however you like, as long as the client can connect. 
Two limitations:
* If you don't change the test scripts you should run the server on port 7070
* You should start the server in json mode, since the client will ask for the server output (test-analysis only parses json files and needs the server output in some cases)

Example command for starting the server:
```
iperf3 -s -p 7070 --json
```

### Getting the test results

All generated iPerf3 logs will be saved as JSONs inside the `iperf-logs` directory. I suggest to always move old results out of that directory once tests are done, and put them inside the `raw-test-results` directory of the repository root.

## test-images
.. contains the relevant images set up for the tests.
The images are kept as basic as possible to reduce the amount of side effects that can possibly happen.
There are build scripts located inside the `test-images`, so the containers have the correct names that are used inside the docker-compose files for the actual tests.

Docker images built with Docker version 27.2.1, build 9e34c9bb39.


## test-analysis
.. contains scripts for analysing gathered iperf3 json logs.

The scripts are kept in python, explanations are inside the code.
To use the scripts you need for example a virtual python environment with the `pandas` and the `matplotlib` libraries installed.
You will also have to edit the paths to the raw test files inside the python code to use everything, as well as the output directory. 
*Important*: The python script won't create folders for you, you have to create them in advance. 

## test-result-graphs
.. contains generated graphs from the test-analysis.
