## Timeline

The target date is to publish an arXiv article on December 1, 2024.

The article will include 
- Specifications of each benchmark task
- Outlines of each submitted system's general architecture, compute process, and measurement methodology
- A table of results including all submissions

TODO: After this, results will be officially collected and announced annually.

## Submission Procedure

TODO

Submitters may choose to publish a more comprehensive report for their own system, citing the NeuroBench specifications. Note that if these results are officially submitted to NeuroBench, they may be subject to audit (see Auditing Process below).

## General Rules

The following general rules are adapted from MLPerf Inference.

- Strive to be fair. The benchmark results should attempt to capture the system's performance and efficiency as fairly as possible.
- The use of evaluation data in model training and system tuning is not allowed. Only training and validation data may be used.
- Replicability is mandatory. Results that cannot be replicated are not valid results. An average over 5 trials must be within 5% of the reported results.
- Submitters may report many results under different system configurations (e.g., performance-focused or efficiency-focused), however in all configurations, all metrics must be reported.
- All submissions are subject to the possibility of an audit by NeuroBench, at its discretion. Submitters may request that another submission is audited.

## Benchmarks

The benchmark specifications can be found in the ASC and QUBO files.

## Auditing Process

Each NeuroBench system track submission is subject to be audited after results are collected. During the auditing process, the results may be temporarily removed or marked as Under Audit on the official leaderboard.

### NDA

A non-disclosure agreement (NDA) should be signed between the auditor and submitter. The auditor will be a third-party who does not have any financial or competitive interests with any of the submitters.

### Access

The submitter must make the system, as well as any required measurement utilities, available for the auditor through a gift or loan, or the auditor will purchase the system and utilities at the submitter's expense.

If the system cannot be gifted, loaned, or purchased, then the submitter should grant remote access to the auditor. If this is also not possible, then the submitter may screen-share the console connected to the system and execute commands as directed by the auditor.

The submitter must also share all software and documentation necessary for reproducing the results, including workload execution and measurement.

### Audit Process

The auditor will verify the submitted results and methodology.

For results, the auditor will try a maximum of 5 times to replicate the submitter's claimed results using the submitter's device and software. If the averaged results are not within 95% of the claimed results, the submitter will be required to either use the auditor's result as the official result, or generate a new result which is at most 5% greater than the auditor's result.

For methodology, the auditor will inspect the documentation of the measurement utilities. The auditor will determine whether the measurements faithfully and fairly capture the performance and efficiency of the system as outlined by the benchmark rules as well as by the report written by the submitter. The auditor may attempt to verify the measurement by using tools such as a multimeter for full-system wall-power analysis.

The auditor may request that the power measurement is updated to include further components or power domains, and/or that the submitter's report is modified to better reflect the methodology. Otherwise, the submitted power/energy result may be removed from the official leaderboard or flagged as an Incomplete Measurement.