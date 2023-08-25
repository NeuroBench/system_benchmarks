# Benchmark Spec Template

Written by: Elias Arnold, Sebastian Billaudelle, Heidelberg University

## Benchmark task name and dataset
Intensity modulation / direct detection (IM/DD) (Task will be published on GitHub soon).
The task concerns the recovering (demapping) of impaired (non-linearity and noise) bits send through an (simulated) optical communication setup with neural networks while minimizing the bit error rate (BER).

## Task scenarios
Single stream

## Applicable systems from represented
BrainScaleS-2

## Model / algorithm that each above system will run
SNN with one hidden LIF and a leaky-integrator output layer with max-over-time decoding, trained with surrogate gradients or EventProp.
A purely spiking SNN with a spiking output layer and time-to-first-spike decoding is also thinkable.

## Metric: correctness / inference quality (and threshold, if applicable)
A minimum BER of 10e-3 at 20 dB SNR.

## Metric: speed or throughput
- Maximum throughput to be determined from demapping of a test set with appropriate size
- For this benchmark the throughput is equivalent to the effective bit rate and can be inferred from sample spacing within a batch of test data.
- Latency could be determined as the duration from time of first input spike to stable classification response of the ASIC .

## Metric: energy / power
Average energy per demapped sample is  derived from active power of full BrainScaleS-2 ASIC at maximum throughput and minimum bit error rate.
The spike encoding and decoding will be performed on the host compute and will not be considered in the energy measurements.

## Measurement protocol details
See above.

## Other notes
- Preprocessing of real-valued data to spike times in a linear fashion  on host computer
