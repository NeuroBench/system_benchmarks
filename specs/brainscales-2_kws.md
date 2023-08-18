# Benchmark Spec Template

Written by: Sebastian Billaudelle, Elias Arnold, Heidelberg University

based on Innatera's specification for the same dataset

## Benchmark task name and dataset
SHD (pre-encoded) and potentially "Aloha" dataset with similar encoding

## Task scenarios
Single stream

## Applicable systems from represented
BrainScaleS-2

## Model / algorithm that each above system will run
Recurrent SNN potentially with adaptive neurons, likely voltage-based readout layer with max-over-time or sum-over-time encoding

## Metric: correctness / inference quality (and threshold, if applicable)
Top 1 accuracy, threshold ~80% as in the original publication

## Metric: speed or throughput (and threshold if applicable)
- maximum throughput to be determined from classification of whole test set
- note: throughput figures have to consider the inhomogeneous durations of samples, potentially report as acceleration in comparison to realtime
- latency (albeit more a property of the task and potentially en-/decoding) could be determined duration from time of first input spike to stable classification response of the ASIC

## Metric: energy
Average energy per inference derived from active power of full BrainScaleS-2 ASIC at maximum throughput and accuracy.
The dataset already ships with spike data, no non-trivial processing is required. FPGA and host system can thus be excluded from the benchmark.

Result from individual supply rails could be used to argue for potential savings but total power should be considered for energy figure.

## Measurement protocol details
See above.

## Other notes

- Disclose computational complexity of off-chip contributions (should be negligible for SHD dataset)
