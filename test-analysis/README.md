# Test Analysis

Python scripts for analysing the gathered test results.

## `two_plots.py`

This is mainly for test results that weren't under network conditions.
Will output some base statistics for throughput, retransmits (tcp), rtt (tcp), jitter (udp), lost packets (udp).

You can configure some settings for the results such as the input/output file paths in the first lines of the scripts.

## `two_plots_unreliable.py`

This is for results on unreliable network conditions, and will output additional graphs that show individual interval statistics (for example how the throughput changed during the time of the tests, to show changes during introduction of unreliable network conditions).

The raw test results for this should be created using the `run_tests_unreliable.sh` scripts in the `data-gathering` directories.

You can configure some settings for the results such as the input/output file paths in the first lines of the scripts.

## `testparser.py`

Only used for reading in iPerf3 json results. Classes for UDP and TCP each, so it's more easy to differentiate.

## `run.py`
Legacy script, do not use. Only still here for old results (personal use).