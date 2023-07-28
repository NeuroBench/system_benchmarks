# Benchmark Spec Template

Written by: 

## Benchmark task name and dataset


## Task scenarios
- _Offline: all samples sent at once_
- _Server: Poisson distribution of queries_
- _Single-stream: one query at a time_

## Applicable systems from represented

## Model / algorithm that each above system will run

## Metric: correctness / inference quality (and threshold, if applicable)

## Metric: speed or throughput (and threshold if applicable)
- _Offline: throughput in samples/second_
- _Server: max throughput in queries/second_
- _Single-stream: latency, 90%-ile or avg over many runs_

## Metric: energy / power
- _Offline and server: average and peak system power_
- _Single-stream: energy per inference_
- _Idle power (?)_

## Measurement protocol details

## Other notes
