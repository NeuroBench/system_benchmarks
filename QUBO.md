# Quadratic Unconstrained Binary Optimization (QUBO) Benchmark Specifications

## Quadratic Unconstrained Binary Optimization (QUBO)

**Quadratic Unconstrained Binary Optimization** refers to the problem to find the binary variable assignment $x_i\in\{0, 1\}$ that optimizes the quadratic cost function

$$ \min_{\mathbf{x}\in\{0,1\}^n} c(\mathbf{x}) = \min_{\mathbf{x}\in\{0,1\}^n} \mathbf{x}^T\mathbf{Q}\mathbf{x}$$

subject to no constraints.



## Benchmark Dataset

### Approximating Maximum Independent Set

The solvers for QUBO will be benchmarked using **Maximum Independent Set** workloads. Given an undirected graph $\mathcal{G}=(\mathcal{V}, \mathcal{E})$, an **independent set** $\mathcal{I}$ is a subset of $\mathcal{V}$ such that, for any two vertices $u, v \in \mathcal{I}$, there is no edge connecting them, i.e., $\nexists \; e \in \mathcal{E} \;s.t.\; e=(u,v) \;\vee\; e=(v,u)$. 
The Maximum Independent Set (MIS) problem consists in finding an independent set with maximum cardinality, as illustrated in the following figure:

<figure>
  <img src="https://github.com/lava-nc/lava-optimization/assets/86950058/53accd20-744a-4e36-b4dd-ccd17af44534" width="750" alt="A maximum ind"/>
<!--   <figcaption>This is the caption for the image.</figcaption> -->
</figure>

The MIS problem has a natural QUBO formulation: for each node $u\in\mathcal{V}$ in the graph, a binary variable $x_u$ is introduced to model the inclusion or not of $u$ in the candidate solution. Summing the quadratic terms $x_u^2$ will thus result in the size of the set of selected nodes. To penalize the selection of nodes that are not mutually independent, a penalization term is associated to the interactions $x_ux_v$ if $u$ and $v$ are connected. The resulting $\mathbf{Q}$ matrix coefficients are defined as

$$
q_{uv} = \begin{cases}
    -1 &\text{if } u = v \\
    4 &\text{if } u \neq v \text{ and } (u, v) \in \mathcal{E} \\
    0 & \text{otherwise.}
\end{cases}
$$

The MIS problem is NP-hard and intractable, and therefore any solver system approximates a solution. Therefore, the cost of the QUBO formulation ($\mathbf{x}^T\mathbf{Q}\mathbf{x}$) is used to assess solutions, and solutions are not restricted to being *maximum* nor *independent sets*. The QUBO formulation ensures that any non-independent set will always have a higher cost than a corresponding independent set with conflicting nodes removed.

### Workloads

The benchmark's workload complexity is defined such that it can automatically grow over time, as neuromorphic systems mature and are able to support larger problems.

- Number of nodes, spaced in a pseudo-geometric progression: 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, ...
- Density of edges: 1%, 5%, 10%, 25%
- Problem seeds: 0, 1, 2, 3, 4 are allowed for tuning. At evaluation time, for official results NeuroBench will announce five seeds for submission. Unofficial results may use seeds which are randomly generated at runtime.

Each workload will be associated with a target optimality, which is the minimum cost found using a conventional solver algorithm.

Small QUBO workloads with fewer than 50 nodes will be solved to global optimality, corresponding to the true maximum independent set.

Larger workloads cannot be reasonably globally solved. The [DWave Tabu CPU sampler](https://docs.ocean.dwavesys.com/projects/tabu/en/latest/intro.html) will be used with 100 reads and 50 restarts, and the QUBO solution with the best cost (best-known solution, BKS) found will set the target optimality for the tuning workload seeds. For evaluation workload seeds, the same method will be used to set the target optimality. 
NeuroBench will provide target optimalities for workloads up to 5000 nodes. Submissions are encouraged to continue scaling up the workload size along the pattern to demonstrate the capacity of their systems. The first group that tackles workloads of an unprecedented size should provide the benchmark solutions via a pull request.

The dataset workload generator and scripts for the DWave Tabu sampler to compute optimal costs are available in the QUBO sub-directory of this repo.

This code is expected to be used as the front-end data generator for all submissions. Submitters may take the general graph descriptions and modify the structure (e.g., load into custom data structures), this is not included in the reported results.
The code also supports arbitrary workload generation, which is expected to be used to measure the largest supported workload size of the system (see Task and Metrics).

## Task and Metrics

Based on the BKS found for each workload, the BKS-Gap optimality score of the solution found by the SUT is defined as
$$
\text{BKS-Gap} = (\frac{c - c_{\mathrm{target}}} {c_\mathrm{target}})\ ,
$$ 
where $c_\mathrm{target}$ is the QUBO cost of the BKS, and $c$ is the cost found by the SUT. This may be reported as a percentage gap by multiplying by 100. If the SUT manages to beat the BKS, then the BKS-Gap will be negative.

The QUBO task can be solved under two task scenarios, using the same workload generator as described above. The first scenario is fixed-timeout (FT), and the second scenario is time-to-solution (TTS).

### Task Scenario 1: Fixed-Timeout (FT)

Given each workload, the benchmark should report the BKS-Gap of the solution found by the SUT after a fixed runtime. The time begins after the graph has been loaded into the SUT. 

Timeouts spread across orders of magnitude ($10^{-3}$, $10^{-2}$, $10^{-1}$, $10^{0}$, $10^{1}$, $10^{2}$). As the runtime is fixed, no measured timing metric is reported, and submissions should report **average power** over the duration of the runtime, as it is directly proportional to energy consumed. The power is averaged over the 5 seeds for each workload. 

Importantly, the QUBO solver needs a module to measure the cost of its solutions, and this module should be considered as part of the SUT, thus its power must be included in the benchmarking results.

### Task Scenario 2: Time-to-Solution (TTS)

Given each workload, the benchmark should report the SUT **latency** and **energy** to meet BKS-Gap thresholds of 0.1, 0.05, and 0.01. If the SUT fails to reach the score thresholds, no result is reported.

For latency, the time begins when the workload graph has been loaded to the system, and ends when the solver has detected target optimality.

Energy measurements identify the energy required to reach each threshold, and is calculated as the average power consumed since the start of the workload (loaded to the system), multiplied by the latency to reach the score threshold. 

As is the case for the FT scenario, the solver needs to include a module that tracks the cost of considered solutions, to identify if it has reached the target optimality. The computational demand and energy for this module must be included in the benchmarking results. 

For both task scenarios, the power measurement should include all computational components, memory, and power domains which are active during the workload processing.

Ultimately, as neuromorphic systems are not matured, a singular power measurement method cannot be applied to all submissions. It is the responsibility of the submitter to faithfully capture all active processing components for their system and fairly outline their methodology in the report. Official submissions are subject to potential audits during which an auditor will inspect the methodology and request additions or revisions to the results and report if necessary.

No other constraints are placed on the algorithmic implementation, nor the hardware setup of the solver system. The system may process the workload using any internal representation, but it must produce the binary vector $\mathbf{x}$ which is used to calculate solution cost $\mathbf{x}^T\mathbf{Q}\mathbf{x}$ as defined above. 

Algorithm and system parameter tuning is restricted, see Tuning below.


### Maximum supported workload size

Separately from the benchmark dataset, the submission should also report the largest supported workload size for the given system, at both 1% edge density and 100% edge density (fully connected). The result are the greatest values $A$ and $B$ such that the workloads $(node, density, seed)$ of $(A, 1\\%, 0)$ and $(B, 100\\%, 0)$ can be loaded onto the system and a solution can be found which is better than the trivial solution of cost 0.

## Tuning

Submitters should only use problem seeds 0, 1, 2, 3, 4 for tuning the parameters of their system and algorithm. Submitters may use workloads with a different number of nodes and/or density than those present in the dataset, though only the values included in the dataset should be reported as official results.

Submitters are not allowed to individually tune their system and algorithmic parameters based on each workload. Any parameters must be some constant value across all workloads, or they may be some function of the workload number of nodes and edge density. The function must not depend on the random seeds used to create the workload or to run the solver, i.e., it must provide the same algorithmic parameters for all problem seeds for a given number of nodes and density. The same function must further be applicable to arbitrary workload sizes and edge densities.
