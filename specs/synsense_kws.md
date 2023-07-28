# Benchmark Spec Template

Written by: Dylan Muir, Synsense

## Benchmark task name and dataset
Heidelberg Digits

Spiking Heidelberg Digits can be used to skip pre-processing


## Task scenarios
Single-stream

## Applicable systems from represented
Xylo Audio, …

## Model / algorithm that each above system will run
Open; custom SNNs

## Metric: correctness / inference quality (and threshold, if applicable)
F1 Multi-class accuracy

Min. threshold 90%?


## Metric: speed or throughput (and threshold if applicable)
Median detection latency from onset of sample

Max latency XX ms


## Metric: energy / power
Idle power (configured system, no data I/O)

Active average power over


## Measurement protocol details
Minimum XX samples

Minimum XX seconds of inference time

## Other notes
Report best-case power, not optimised for performance?;

Best-case performance, not optimised for power (but report power as well);

Power at performance target (match target performance)
