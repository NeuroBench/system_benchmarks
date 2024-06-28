# Quadratic Unconstrained Binary Optimization for Maximum Independent Set (QUBO-MIS) Benchmark Specifications

## Benchmark Dataset

Given an undirected graph $\mathcal{G}=(\mathcal{V}, \mathcal{E})$, an \emph{independent set} $\mathcal{I}$ is a subset of $\mathcal{V}$ such that, for any two vertices $u, v \in \mathcal{I}$, there is no edge connecting them, i.e., $\nexists \; e \in \mathcal{E} \;s.t.\; e=(u,v) \;\vee\; e=(v,u)$. 
The **Maximum Independent Set (MIS) problem** consists in finding an independent set with maximum cardinality, as illustrated in the following figure:

<figure>
  <img src="https://github.com/lava-nc/lava-optimization/assets/86950058/53accd20-744a-4e36-b4dd-ccd17af44534" width="750" alt="A maximum ind"/>
<!--   <figcaption>This is the caption for the image.</figcaption> -->
</figure>

The MIS problem has a natural QUBO formulation: for each node $u\in\mathcal{V}$ in the graph, a binary variable $x_u$ is introduced to model the inclusion or not of $u$ in the candidate solution. Summing the quadratic terms $x_u^2$ will thus result in the size of the set of selected nodes. To penalize the selection of nodes that are not mutually independent, a penalization term is associated to the interactions $x_ux_v$ if $u$ and $v$ are connected. The resulting $\mathbf{Q}$ matrix coefficients are defined as

$$
q_{uv} = \begin{cases}
    -1 &\text{if } u = v \\
    \lambda &\text{if } u \neq v \text{ and } (u, v) \in \mathcal{E} \\
    0 & \text{otherwise}
\end{cases}
$$

where $\lambda>0$ is a large penalization term provided by the problem formulation. 

The benchmark's workload complexity is defined such that it can automatically grow over time, as neuromorphic systems mature and are able to support larger problems.

- Number of nodes, spaced on a logarithmic scale: 10, 25, 50, 100, 250, 500, ...
- Density of edges: 1%, 5%, 10%, 25%
- Problem seeds: 0, 1, 2, 3, 4 are allowed for tuning. At evaluation time, for official results NeuroBench will announce five seeds for submission. Unofficial results may use seeds which are randomly generated at runtime.

Each evaluation workload will be associated with a target optimality, which is the size of the largest independent set found using a conventional solver algorithm.

Small QUBO workloads with fewer than 1000 nodes will be solved to global optimality, corresponding to the true maximum independent set.

Larger workloads cannot be reasonably globally solved. The DWave Tabu sampler will be used with 100 reads and 50 restarts, and the QUBO solution with the best cost found will set the target optimality for the tuning workload seeds. For evaluation workload seeds, the same method will be used to set the target optimality. The NeuroBench authors will provide benchmarking CPU solutions up to 5000 nodes. The first group that tackles workloads of an unprecedented size should provide the benchmark solutions via a pull request.

Code for the generator for MIS, as well as a wrapper to run DWave's Tabu search, is located here: [https://github.com/NeuroBench/system_benchmarks/tree/qubo/qubo_generator](https://github.com/NeuroBench/system_benchmarks/tree/qubo/qubo_generator).

This code is expected to be used as the front-end data generator for all submissions. Submitters may take the general graph descriptions and modify the structure, this is not included in the reported results.
The code also supports arbitrary workload generation, which is expected to be used to measure the largest supported workload size of the system (see Task and Metrics).

## Task and Metrics

Given each workload, report the latency and energy to meet optimality thresholds. The average over 5 seeds for each workload is officially listed, as well as standard error. Results for all 5 seeds should be included in the submission report.

The solver needs to include a module that tracks the cost of considered solutions, to identify if it has reached the target optimality. The computational demand and energy for this module must be included in the benchmarking results. Apart from this, no constraints are placed on the algorithmic implementation, nor the hardware setup. Algorithm and system parameter tuning is restricted, see Tuning below.

### Optimality Thresholds

Based on the target optimality $c_\mathrm{target}$ for each workload, the normalized optimality score of a solution is defined as 

$$
\mathrm{abs}(\frac{c - c_{\mathrm{target}}} {c_\mathrm{target}})\ .
$$ 

Where $c$ is the cost of the best solution to the QUBO found by the system at that point in time.

The score thresholds are 0.1, 0.05, and 0.01.

For each threshold, the submission reports the solution, the cost of the best solution, latency between start of the solver and finding the reported solution, and system energy.

If the system does not reach the score threshold, no result is reported. All problem seeds must reach a score threshold in order for the result to be included in the official leaderboard, otherwise that particular result will be left blank.

### Latency

Latency measures the time taken in order for the system to reach the defined score thresholds.

The time begins when the workload graph has been loaded to the system. It ends when the solver has detected target optimality. The time needed to transfer the solution to an external host is excluded from the benchmarking results, unless the solver needs post-processing on the host to identify the solution or its cost.

### Energy

Energy measurements identify the energy required to reach each defined score threshold.

The energy is caluclated as the average power consumed since the start of the workload (loaded to the system), multiplied by the latency to reach the score threshold.

The power measurement should include all computational components, memory, and power domains which are active during the workload processing.

Ultimately, as neuromorphic systems are not matured, a singular power measurement method cannot be applied to all submissions. It is the responsibility of the submitter to faithfully capture all active processing components for their system and fairly outline their methodology in the report. Official submissions are subject to potential audits during which an auditor will inspect the methodology and request additions or revisions to the results and report if necessary.

### Maximum supported workload size

Separately from the benchmark dataset, the submission should also report the largest supported workload size for the given system, at both 1% edge density and 100% edge density (fully connected). The result are the greatest values $A$ and $B$ such that the workloads $(node, density, seed)$ of $(A, 1\\%, 0)$ and $(B, 100\\%, 0)$ can be loaded onto the system and a solution can be found which is better than the trivial solution of cost 0.

## Tuning

Submitters should only use problem seeds 0, 1, 2, 3, 4 for tuning the parameters of their system and algorithm. Submitters may use workloads with a different number of nodes and/or density than those present in the dataset, though only the values included in the dataset should be reported as official results.

Submitters are not allowed to individually tune their system and algorithmic parameters based on each workload. Any parameters must be some constant value across all workloads, or they may be some function of the workload number of nodes and edge density. The function must not depend on the random seeds used to create the workload or to run the solver, i.e., it must provide the same algorithmic parameters for all problem seeds for a given number of nodes and density. The same function must further be applicable to arbitrary workload sizes and edge densities.
