### General

- System name
- Organization
- Submission date
- Availability 
	- Available (for purchase, rent, cloud access)
	- Preview (must be submitted as Available in next round)
	- RDI (research, development, internal)
- Power measurement device(s)
	- External analyzer tap
	- On-board instrument
	- Wall power system measurement
	- Estimate (only for simulated systems, or a potential downgrade of the result after audit)
- Configuration (optional if multiple)
	- Performance
	- Efficiency
- Software

TODO/?: Static/floor power, Host CPU, Model/Algorithm name

### ASC

- Evaluation set accuracy
- Energy in uJ
- Latency in ms

### QUBO-MIS

- Maximum supported graph size, fully connected
- Maximum supported graph size, 1% density

- For each workload (nodes, density, target_optimality), over 5 seeds:
	- Time and energy to reach 90% of target_optimality
	- Time and energy to reach 95% of target_optimality
	- Time and energy to reach 99% of target_optimality

- (Optional) Exceeded target_optimality, one seed per workload size:
	- Seed
	- Optimality achieved
	- Time and energy to reach