# Report

All official benchmark submissions should be associated with a report which includes the information described here. The purpose of the report is to provide context for the benchmark submission results, as the overall benchmark format is generally open and does not have stringent consistency rules.

Submitters should strive to be fair and faithful in their depiction and description of their system and results.

The report will be linked in the official leaderboard, and included in its entirety in official results publication.

Official submissions are subject to the possibility of an audit, in which case not only the submitted results, but also the associated report may be inspected. See the Auditing Process in the Rules document.

## Requirements (TODO)

- An outline of the system architecture
- An outline of the algorithm used (model architecture, tuning)
- A diagram depicting the workflow, including (where applicable) data initialization, host pre-processing, data loading, on-device preprocessing, inference, post-processing
- Latency measurement description
- Power measurement description
	- Device used (name?) (External analyzer tap, on-board instrument, wall power system measurement)
	- Which components / functionalities are included, and which are omitted
	- Power measurement time resolution / frequency
- Re-iterate results
	- Including separation into pre-processing and inference, if applicable
	- TODO: Separation of static and dynamic power? This should be stated as floor power since we only measure during activity?