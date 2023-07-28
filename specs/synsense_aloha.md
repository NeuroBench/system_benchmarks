# Benchmark Spec Template

Written by: Dylan Muir, Synsense

## Benchmark task name and dataset
Aloha wake-phrase detection



## Task scenarios
Single-stream

## Applicable systems from represented
Xylo, Innaterra SNP, Loihi, …

## Model / algorithm that each above system will run
Open; custom SNNs

## Metric: correctness / inference quality (and threshold, if applicable)
Miss rate (max. XX% per sample)

False detection rate (under google speechcommands?) (max. XX% per sample)

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
