# Acoustic Scene Classification (ASC) Benchmark Specifications

## Benchmark Dataset

The benchmark considers the classification of audio samples of various environments.

The dataset is based on the DCASE 2020 acoustic scene classification challenge ([link](https://dcase.community/challenge2020/task-acoustic-scene-classification)), using the TAU Urban Acoustic Scenes 2020 Mobile datasets.

Of the 10 available scene classes, 4 are used: "airport", "street_traffic", "bus", "park"

Of the 9 real / simulated recoding devices, 1 real device is used: "a"

Audio samples are sliced into 1 second samples. The audio may be resampled to a different frequency as a pre-processing step, which is not included in inference measurement.

The train/val/test split is 41360/1320/16240 samples.

A NeuroBenchDataset (PyTorch) compliant dataset file is available here: https://github.com/NeuroBench/system_benchmarks/blob/audio_scene_classification/utils/dcase_audio_scene_classification.py

A download script for the data is also available here: https://github.com/NeuroBench/system_benchmarks/blob/audio_scene_classification/utils/download_dcase_dataset.py

This code is expected to be used as the front-end data generator for all submissions. The data may be reformatted into a different framework, this is not included in inference measurement.

## Task and Metrics

After training a model using the training and validation set, the submitter will report test set accuracy, as well as latency and energy per inference on the system. 

Audio samples will be processed in batch-size 1, in which one sample is processed at a time and the next sample is not processed until the previous one is finished.

The general compute flow consists of three steps: pre-processing, inference, and classification. 

One inference is defined as the processing of one second of audio data. Inference is separate from classification because systems are often intended to process samples as sequences over time, rather than all at once, and the classification may be available before the whole data sequence is seen. Classification thus does not need to be included in the benchmark measurement.

Pre-processing in general can be defined as feature extraction or the conversion of raw audio data into a format that is suitable for inference. Latency and energy of pre-processing must be included in benchmark measurement, and will be reported separately from inference. 

In certain systems, e.g. Synsense Xylo, pre-processing blocks use analog hardware on-chip to directly convert real-time analog microphone output to digital spikes for inference. In order to operate inference from a digitally-encoded dataset, this pre-processing must be simulated and the spikes are sent through a side-channel directly to the inference block. For such cases, the reported pre-processing measurements will be for the analog hardware running in real-time, and not the simulated side-channel. TODO: how will the measurement be done, need some kind of disclaimer in the report that the result will not be completely reflective of the dataset.


### Accuracy

Accuracy of the predictions on the test set, measured from the system and not in any software simulation.

### Latency

Latency is the average time per pre-processing and inference. The final result should be averaged over all samples in the test set, and include standard error.

The time begins when data has been loaded into on-board or on-chip memory and is prepared to be processed. The time ends when the last timestep of the sequence has completed processing.

### Energy

TODO: define power / energy metric and how it should be measured / calculated. 

1. How is floor/static power measured, is this converted to floor/static energy?
2. Any processing units which should be included / not necessarily included?

The energy consumed in any given processing is calculated as the average power during the inference multiplied by the latency of the inference. The submitter should report the average energy over all samples, including standard error.

The power measurement should include all computational components and power domains which are active during the workload processing. This includes:

- TODO: specific things which should be included / not needed to be included (e.g. memory)

Ultimately, as neuromorphic systems are not matured, a singular power measurement method cannot be applied to all submissions. It is the responsibility of the submitter to faithfully capture all active processing components for their system and fairly outline their methodology in the report. Official submissions are subject to potential audits during which an auditor will inspect the methodology and request additions or revisions to the results and report if necessary.

