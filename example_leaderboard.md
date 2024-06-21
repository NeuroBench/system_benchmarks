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
[//]: # (allow for "shunt" explicitly as an external measurement point?)
[//]: # (also: point of measurement vs. measurement device => orthogonal points)
	- On-board instrument
[//]: # (definition of possible measurement points? (e.g. total ASIC power, total system power))
[//]: # (minimum number of samples per "run" (for the "fast" systems) and minimum frequency (for the "slow" systems) required)
[//]: # (limit of ratio: (capacity / ~~power~~ avg. current in) (i.e. sum up caps on PCB… O(uF) is reasonable, everything above problematic?))
[//]: # (reasoning/example: 1/2 C U^2, e.g. at 10mF, dV = 1V => 5mJ similar OoM than 10ms run at P=10W active consumption!)
[//]: # (measurments should last long to exclude capacitic effects)
[//]: # (e.g. multiple back-to-back (<10% inter-run time gaps) runs or repetitive inputs? aim for O(10s) measurement time)
	- Wall power system measurement
[//]: # (percent-preciscion but typically way too slow for non-equilibrium measurements? → capacity is a problem! at least DC measurement needed (because at 50Hz ms-resolution after a PSU is "insane" (quoting our hardware guy)!))
	- Estimate (only for simulated systems, or a potential downgrade of the result after audit)
[//]: # (how to flag "measurement complete"?)
[//]: # (baseline measurements? e.g. configure system and then measure idle, empty/dummy runs w/o data (btw. idle-after run measurement even worse in terms of capacitic effects))
- Configuration (optional if multiple)
	- Performance
	- Efficiency
- Software

TODO/?: Static/floor power, Host CPU, Model/Algorithm name

### ASC

- Evaluation set accuracy
- Power in SI units
- Energy in SI units
- Latency (= inverse bandwidth?) in SI units
- Latency in SI units

### QUBO-MIS

- Maximum supported graph size, fully connected
- Maximum supported graph size, 1% density

- For each workload (nodes, density, target_optimality), over 5 seeds:
[//]: # (auditor chooses 5 random seeds?)
	- Time and energy to reach 90% of target_optimality
	- Time and energy to reach 95% of target_optimality
	- Time and energy to reach 99% of target_optimality

- (Optional) Exceeded target_optimality, one seed per workload size:
	- Seed
	- Optimality achieved
	- Time and energy to reach