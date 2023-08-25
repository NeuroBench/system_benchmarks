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

### Power measurement
The power measurement details for SpiNNaker2-based systems are different depending on the addressed form factor (e.g., Edge or Large-scale):

* Single-chip board (Standalone):
  - On-board processor: There is a Python-assisted approach via a simple interface in which an on-board STM microcontroller employs measurements at the shunt voltages to estimate the power drawn on the supply voltages of the chip.
* 48-node board (Standalone):
  - At the power adapter: It implies using a Lab power supply. This is the most accurate way to estimate the power as the power supplies typically have a good resolution but involves a manual process, which is not simple to automate with a harness.
  - On-board processor: Similarly to the single-chip case, the on-board processor of the 48-node board collects the measurement points from each DC-DC converter corresponding to a subset of chips within the 48-node mesh. These values are then transmitted to the host via the ST-link debugger cable.
* Full system (More than 1 card-frame): A SpiNNcloud supercomputer is composed by a large number of 48-node boards, which are hosted within card-frames, each card-frame having 18 boards.
  - On-board processor: The process is similar to the standalone boards, but it involves the communication of a series of on-board processors. Every card frame has an ST-based on-board processor that is the central point to read the Power Management bus of two supplies that are providing power in an interlaved scheme to the full card-frame. Such processor communicates to the host to report the power during a particular testcase. The same process applies for larger systems but it requires the host to communicate to all on-board processors in every card-frame

### Benchmark execution

The sequence for executing SNN on SpiNNaker2 is:
1. Create SNN with parameters, weights, input sikes; map (partition) SNN  to
   hardware, and generate experiment specification.
2. Intialize hardware.
3. Load binaries of ARM cores and parameters to chip, start ARM cores to
   initialize.
4. Load input data from host to hardware.
5. Execute experiment on hardware triggered by Host. Experiment on the hardware
   runs standalone for pre-defined time.
6. Read results from hardware to host.
7. Postprocess results and provide to user frontend.

* For multiple experiments with changed input, e.g., data samples, steps 4 to
  6 are repeated. With more engineering, all input data and results could be stored in DRAM.
* **Power measurements** can be done either only during step 5, but also from
  from steps 2 to 6 if required.
* **Time measurements:** the execution time of an SNN on SpiNNaker2 depends on
  the number of timesteps and hence is fixed beforehand due to real-time
  simulation. Yet the duration of a time step can be optimized. One could also
  measure the full execution time (steps 1-7) or including loading input and
  results (steps 4-6).

## Other notes
The preprocessing requirements of this task are minimal as it needs only the adjacency matrix. However, passing through the list of samples could be different between different platforms.

Having a benchmark harness would facilitate the execution of the benchmark. Specifically for SpiNNaker2-based systems, the host (Python or CPP) could be used as part of the benchmark harness. It's purpose would be to generate and preload the data into the DRAM using either the offline or single-stream approach, provide an execution environment to run the benchmark, monitor the execution of the benchmark, and read back the results to calculate and summarize the benchmark outcome.

For the specific QUBO task, it would be important to agree on the exact parameters (e.g., injecting similar noise partners: for example,
either injecting noise into a single neuron or a population of those).


