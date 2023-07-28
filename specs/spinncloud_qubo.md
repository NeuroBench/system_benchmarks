# Benchmark Spec Template

Written by: Hector Gonzalez, SpiNNcloud

## Benchmark task name and dataset
MaxCut – NP hard problem

Dataset: [Gset (e.g., G15)]
(https://web.stanford.edu/~yyye/yyye/Gset/).

There are different types of graph sizes and
examples with a wide variety of complexity.

## Task scenarios
Offline: all samples are sent at once. Useful for
large-scale graphs.

Single stream: One query at a time

## Applicable systems from represented
Xylo, SpiNNaker 1/2, Loihi1/Loihi2

## Model / algorithm that each above system will run
QUBO via SNN 

## Metric: correctness / inference quality (and threshold, if applicable)
Number of cuts. No threshold, but each dataset
has a corresponding state of the art number of
cuts (e.g., for G15 is 3050)


## Metric: speed or throughput (and threshold if applicable)
Offline: Sampling efficiency, Throughput

Single-stream: Sampling efficiency (not really latency as not all CUTs are discovered)

## Metric: energy / power
Offline: Power

Single-stream: Power

## Measurement protocol details
Same as both MLPerf Tiny and Datacenter
setup depending on whether the scope of the
task is edge or large-scale. It could be both as
the task can be defined to use small or large
graphs.

## Other notes
The preprocessing requirements of this task are
minimal as it needs only the adjacency matrix.

However, passing through the list of samples
could be different between different platforms.

Having a benchmark harness makes sense for
all types of problems. It could include a tool to
generate the data, an execution environment to
run the benchmark, a data collection
component to monitor the execution of the
benchmark, and a reporting component to
calculate and summarize the benchmark
results.

Agreeing on the exact parameters (e.g.,
injecting similar noise partners: for example,
either injecting noise into a single neuron or a
population of those).

The data could reside on a host system and it is
sent according to the scenarios outlined
(Offline or single-stream)

