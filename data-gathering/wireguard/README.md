# WireGuard benchmark tests

## Running

First, create the docker subnet necessary for the containers
```bash
docker network create --subnet 172.20.0.0/24 masqNet
```

Then run the container once:
```bash
docker compose run iperf3
```
This is just to create the initial WireGuard server config. Will be created in `./wireguard-server-config/peer_iperf3client/peer_iperf3client.conf`.
Copy this file as wg0 into `./wireguard-client-config/wg_confs/wg0.conf`.

Afterwards you can start doing tests by running the container, for example:
```bash
docker compose run -e BITRATE=200 -e TESTTIME=60 -e PARALLEL=1 -e TESTCASE="BANDWIDTH_TEST" -e IPERF_SERVER_IP="192.168.0.45" -e CURRENT="UDP-UPLOAD-BANDWIDTH" -e PACKET_SIZE=800 iperf3
```

The environment variables are defined as:
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

Only the `CURRENT` variable is required, which is the name of the test file without the extension.

Note that you have to have a iPerf3 server running on the server IP on port 7070. 
To edit or add test scripts with your own iPerf3 command and tc settings, put them in `./iperf-tests/`. They have to end in `.sh`.
There are also scripts for automatically running a number of tests, look into `run_tests.sh` and `run_rests_unreliable.sh` for that.

## After Running

You should move the test files into a folder in `raw-test-results` in the repositories root.
Note: You will need root for that (the containers access rights aren't correct..)