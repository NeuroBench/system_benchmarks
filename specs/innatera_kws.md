# Benchmark Spec Template

Written by: Peter Bogdan, Innatera

## Benchmark task name and dataset
KWS, SHD (pre-encoded)

## Task scenarios
Single stream

## Applicable systems from represented
SNP, ...

## Model / algorithm that each above system will run
???

- Likely proprietary to system
- **TODO**: What should be reported for systems if they have custom processing pipelines?
	- Algorithm complexity metrics?

## Metric: correctness / inference quality (and threshold, if applicable)
Top 1 accuracy, threshold ~80% as in the original publication

## Metric: speed or throughput (and threshold if applicable)
Latency definition: from data in memory back to inference result in memory (average over multiple runs)
- Note: memory is not well defined over all systems?

Report: System clock speed --> inference latency


## Metric: energy / power
Average power per inference

## Measurement protocol details

## Other notes

- Disclose what is computed on- vs off-device
- Start when data enters processing pipeline, end when inference result reported (in memory, on pin)
- Power: what components are included in measurement?
- For large scale systems when full capacity is not used, how to measure performance?

