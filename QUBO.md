# Quadratic Unconstrained Binary Optimization for Maximum Independent Set (QUBO-MIS) Benchmark Specifications

## Benchmark Dataset

The benchmark considers the maximum indpendent set (MIS) problem: Given an undirected graph, find the largest subset of vertices consisting of mutually unconnected vertices.

TODO: add math text or switch to a different file format that supports it.

The workload complexity is defined such that it can automatically grow over time, as neuromorphic systems mature and are able to support larger problems.

- Number of nodes, spaced on a logarithmic scale: 500, 1000, 2500, 5000, ... TODO: what would be a reasonable starting point?
- Density of edges: 1%, 5%, 10%, 25%
- Problem seeds: 0, 1, 2, 3, 4 are allowed for tuning. At evaluation time, for official results NeuroBench will announce five seeds for submission. Unofficial results may use seeds which are randomly generated at runtime.

Each evaluation workload will be associated with a target optimality, which is the size of the largest independent set found using a conventional solver algorithm.

Small workloads fewer than TODO nodes will be completely solved, and the target optimality will be the size of the globally maximum independent set.

Larger workloads cannot be reasonably globally solved. The DWave Tabu sampler will be used with 100 reads and 50 restarts, and the largest independent set found will set the target optimality for the tuning workload seeds. For evaluation workload seeds, the same method will be used to set the target optimality.

TODO: Should we limit the time that the CPU solver is allowed? 

TODO: Should we allow for the target optimality to be increased if someone finds a larger independent set with CPU / neuromorphic?

Code for the generator for MIS, as well as the DWave Tabu search implementation, is located here: https://github.com/NeuroBench/system_benchmarks/tree/qubo/qubo_generator

This code is expected to be used as the front-end data generator for all submissions. Submitters may take the general graph descriptions and modify the structure, this is not included in the reported results.
The code also supports arbitrary workload generation, which is expected to be used to measure the largest supported workload size of the system (see Task and Metrics).

## Task and Metrics

Given each workload, report the latency and energy to meet optimality thresholds. The average over 5 seeds for each workload is officially listed, as well as standard error. Results for all 5 seeds should be included in the submission report.

No constraints are placed on the algorithmic implementation, nor the hardware setup. Algorithm and system parameter tuning is restricted, see Tuning below.

### Optimality Thresholds

Based on the target optimality c_target for each workload, the normalized optimality score of a solution is defined as (1 / n) * abs((c - c_target) / c_target). 
Where c is the size of the largest independent set found by the system at that point in time.

The score thresholds are TODO, see below

TODO: normalizing by dividing by the graph size makes it so that the 0.1/0.5/0.01 don't make any sense. E.g. for a graph size of 1,000,000 the score would always be on the order of 0.000001. The score needs a different definition. Is there any score that we could use where it's possible to show that you exceed the target?

For each threshold, the submission reports latency (from beginning the workload), and system energy.

If the system does not reach the score threshold, no result is reported. All problem seeds must reach a score threshold in order for the result to be included in the official leaderboard, otherwise that particular result will be left blank.

If the system exceeds the target optimality for any seed for any given workload size, then the submitter may report the seed, set size found, latency, and energy.

TODO: is there any consideration about the time that it takes to check the optimality? is the submitter responsible for tracking the optimality over time, or should they just guess / use trial+error when their solution has reached it? If this checking needs to be inserted during runtime, does it count towards latency/energy?

### Latency

Latency measures the time taken in order for the system to reach the defined score thresholds.

The time begins when the workload graph has been loaded to the system.

### Energy

Energy required to reach each defined score threshold.

The energy is caluclated as the average power consumed since the start of the workload (loaded to the system), multiplied by the latency to reach the score threshold.

The power measurement should include all computational components and power domains which are active during the workload processing. This includes:

- TODO: specific list of things that should be included, or need not be included. 
- TODO: notes about DRAM memory, anything off-chip

Ultimately, as neuromorphic systems are not matured, a singular power measurement method cannot be applied to all submissions. It is the responsibility of the submitter to faithfully capture all active processing components for their system and fairly outline their methodology in the report. Official submissions are subject to potential audits during which an auditor will inspect the methodology and request additions or revisions to the results and report if necessary.

### Maximum supported workload size

Separately from the benchmark dataset, the submission should also report the largest supported workload size for the given system, at both 1% edge density and 100% edge density (fully connected). The result are the greatest values A and B such that the workload (A, 1%, 0) and (B, 100%, 0) can be loaded onto the system and a solution can be found which is better than the trivial solution of size 0.

## Tuning

Submitters should only use problem seeds 0, 1, 2, 3, 4 for tuning the parameters of their system and algorithm. Submitters may use workloads with a different number of nodes and/or density than those present in the dataset, though only the values included in the dataset should be reported as official results.

Submitters are not allowed to individually tune their system and algorithmic parameters based on each workload. Any parameters must be some constant value across all workloads, or they may be some function of the workload number of nodes and edge density which can be scaled to arbitrarily larger workload sizes. Parameters must be the same for all problem seeds for the same number of nodes and density.

TODO: What is meant by a function? Technically, any mapping of workload size to some number is a function. I added that the function must be able to be scaled to arbitrarily larger workloads, but there's probably a more formal way to say this.
