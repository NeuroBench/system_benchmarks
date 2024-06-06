# Acoustic Scene Classification (ASC) Benchmark Specifications

## Benchmark Dataset

The benchmark considers the classification of audio samples of various environments.

The dataset is based on the DCASE 2020 acoustic scene classification challenge [TODO], using the TAU Urban Acoustic Scenes 2020 Mobile datasets.

Of the 10 available scene classes, 4 are used: "airport", "street_traffic", "bus", "park"

Of the 9 real / simulated recoding devices, 1 real device is used: "a"

Audio samples are sliced into 1 second samples. The audio may be resampled to a different frequency as a preprocessing step, which is not included in inference measurement.

The train/val/test split is TODO/1320/13000 samples.

A NeuroBenchDataset (PyTorch) compliant dataset file is available here: https://github.com/NeuroBench/system_benchmarks/blob/audio_scene_classification/utils/dcase_audio_scene_classification.py

This code is expected to be used as the front-end data generator for all submissions. The data may be reformatted into a different framework, this is not included in inference measurement.

## Task and Metrics

After training a model using the training and validation set, the submitter will report test set accuracy, as well as latency and energy per inference on the system.

The samples should be processed in accordance with the MLPerf single stream scenario, during which one sample is processed at a time, and the next sample is not processed until the previous one has finished.

### Accuracy

Accuracy of the predictions on the test set, measured from the system and not in any software simulation.

### Latency

Latency is the average time per inference. The final result should be averaged over all samples in the test set, and include standard error.

The time for each inference begins when data has been loaded into on-board or on-chip memory. TODO: is it safe to assume that the systems will have memory? what if they do not?

If any pre-processing is done on-chip, the latency of this step should be separately measured from the inference. The separate results can be listed in the submitted report, but the official leaderboard will display the aggregated latency of pre-processing and inference.

TODO: what if there is pre-processing on the host?

### Energy

The energy consumed in any given inference is calculated as the average power during the inference multiplied by the latency of the inference. The submitter should report the average energy over all samples, including standard error.

The power measurement should include all computational components and power domains which are active during the workload processing. This includes:

- TODO: specific things which should be included / not needed to be included (e.g. memory)

Like the latency measurement, if any pre-processing components are used, the energy of those components should be separately measured from the inference. The submitted report should list both, and the official leaderboard will display the aggregate energy.

Ultimately, as neuromorphic systems are not matured, a singular power measurement method cannot be applied to all submissions. It is the responsibility of the submitter to faithfully capture all active processing components for their system and fairly outline their methodology in the report. Official submissions are subject to potential audits during which an auditor will inspect the methodology and request additions or revisions to the results and report if necessary.

