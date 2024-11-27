import re
import torch
import numpy as np
import librosa
import pandas as pd
from pathlib import Path
from tqdm.contrib.concurrent import thread_map
from tqdm.notebook import tqdm
from torch.utils.data import Dataset, DataLoader
from neurobench.datasets.dataset import NeuroBenchDataset
import torch.nn.functional as F


class SceneDataset(NeuroBenchDataset):
    def __init__(self, x, y, device='cpu'):
        self.x = x
        self.y = y
        self.device = device
        self.to(self.device)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

    def __len__(self):
        return len(self.x)

    def to(self, device):
        self.x = self.x.to(device)
        self.y = self.y.to(device)

        return self


class SceneData():
    r"""A torch Dataset for loading and preprocessing the dcase scene classification data.
    Args:
        raw_data_dir: The path to the directory where the raw .wav files are stored.
        meta_files_dir: The path to the directory where the train/test/evaluate .csv files are stored.
        valid_scenes: A list containing the scenes (classes) you want to load.
        valid_devices: A list containing the devices you want to use. By default all devices are used.
        target_sample_rate: An int representing the frequency for resampling.
        resize_time: A float value representing the time in second to which each original sample will be split into.
            For example, if the original audio is 10 seconds long, and the resize time is 1, each sample will be split
            into 10 samples in the dataset, each with the original label. The last split sample will be padded with 0s where needed.
            If this value is larger than the actual audio length, the audio file will be loaded as is and no resize will be done.

    Examples:
        >>> dataset = SceneData("~/datasets/raw/dcase/",
        ...           meta_files_dir="~/raw/dcase_meta/",
        ...           valid_scenes=["airport", "street_traffic", "bus", "park"],
        ...           valid_devices=['a'],
        ...           target_sample_rate=8000,
        ...           max_samples_per_scene=10,
        ...           resize_time=1)

    """

    def __init__(self,
                 raw_data_dir,
                 meta_files_dir,
                 valid_scenes,
                 valid_devices=None,
                 max_samples_per_scene=None,
                 target_sample_rate=None,
                 resize_time=None
                 ):
        self.raw_data_dir = Path(raw_data_dir)
        self.meta_files_dir = Path(meta_files_dir)
        self.valid_scenes = valid_scenes
        self.valid_devices = valid_devices
        self.target_sample_rate = target_sample_rate
        self.resize_time = resize_time
        self.num_classes = len(np.unique(self.valid_scenes))
        self.all_files = {}

        self.all_files["train"] = pd.read_csv(self.meta_files_dir / "fold1_train.csv", delimiter='\t')
        self.all_files["test"] = pd.read_csv(self.meta_files_dir / "fold1_evaluate.csv", delimiter='\t')
        self.filtered_files = {"x_train": [], "y_train": [], "x_test": [], "y_test": []}
        self.data = {"x_train": None, "y_train": None, "x_test": None, "y_test": None}

        # Adding extra files
        train_files = np.genfromtxt(self.meta_files_dir / "fold1_train.csv", dtype=str, skip_header=1)[:, 0]
        train_files = np.array([f.split("/")[-1] for f in train_files])  # remove subfolder
        test_files = np.genfromtxt(self.meta_files_dir / "fold1_evaluate.csv", dtype=str, skip_header=1)[:, 0]
        test_files = np.array([f.split("/")[-1] for f in test_files])  # remove subfolder
        all_files = np.array([f.name for f in self.raw_data_dir.glob("*.wav")])
        extra_test_files = np.array(list(set(all_files) - set(train_files) - set(test_files)))
        extra_test_labels = np.array([x.split('-')[0] for x in extra_test_files])
        extra_test_df = pd.DataFrame({"filename": extra_test_files, "scene_label": extra_test_labels})
        self.all_files["test"] = pd.concat([self.all_files["test"], extra_test_df])

        if valid_devices is not None:
            glob_patterns = []
            for device in valid_devices:
                glob_patterns.append(f".*{device}.wav")
        else:
            glob_patterns = [".*.wav"]

        for split in ["train", "test"]:
            for idx, scene in enumerate(valid_scenes):
                x = self._filter_files(self.all_files[split], scene, glob_patterns)
                self.filtered_files[f"x_{split}"].extend(x)
                self.filtered_files[f"y_{split}"].extend([idx] * len(x))

        self._load_all_data()

    def _filter_files(self, files_df, scene, patterns):
        all_scene_files = [x.split('/')[-1] for x in files_df['filename']]
        files_from_recdevice = []
        for pat in patterns:
            exp = re.compile(scene + pat)
            files_from_recdevice.extend([x for x in all_scene_files if exp.match(x)])
        return files_from_recdevice

    def _load_all_data(self):
        for split in ["train", "test"]:
            length = len(self.filtered_files[f"x_{split}"])
            print(f"Loading {split} data:")
            results = thread_map(self._load_data, zip(list(range(length)), [split] * length))
            self.data[f"x_{split}"] = torch.vstack([r for rl in results for r in rl[0]])
            self.data[f"y_{split}"] = torch.vstack([r for rl in results for r in rl[1]])

    def _load_data(self, args):
        idx, split = args
        target_sr = self.target_sample_rate if self.target_sample_rate else 22050
        audio_file_path, label = self.filtered_files[f"x_{split}"][idx], self.filtered_files[f"y_{split}"][idx]
        x, sr = librosa.load(self.raw_data_dir / audio_file_path, sr=target_sr)
        audio_length_s = len(x) / sr
        sample_x, sample_y = [], []

        resize_ratio = 1 if self.resize_time is None else min(self.resize_time / audio_length_s, 1)
        resized_sr = int(len(x) * resize_ratio)
        for r in range(0, len(x), resized_sr):
            resized_x = x[r:r + resized_sr]

            if len(resized_x) < resized_sr:
                orig_size = len(resized_x)
                resized_x = np.pad(resized_x, pad_width=(0, resized_sr - len(resized_x)))

            y = F.one_hot(torch.tensor(label), num_classes=self.num_classes).to(torch.float32)
            sample_x.append(torch.from_numpy(resized_x))
            sample_y.append(y)
        return sample_x, sample_y

    def save_to_file(self, save_dir_path, filename):
        dir_path, f_path = Path(save_dir_path), Path(filename)
        torch.save({
            "x_train": self.data["x_train"],
            "y_train": self.data["y_train"],
            "x_eval": self.data["x_test"],
            "y_eval": self.data["y_test"],
        }, dir_path / (f_path.name + ".pt"))

    def load_from_file(self, file_path):
        data = torch.load(file_path)
        self.data["x_train"] = data["x_train"]
        self.data["y_train"] = data["y_train"]
        self.data["x_test"] = data["x_test"]
        self.data["y_test"] = data["y_test"]

    def get_datasets(self):
        self.train_dataset = SceneDataset(self.data["x_train"], self.data["y_train"])
        self.test_dataset = SceneDataset(self.data["x_test"], self.data["y_test"])

        return self.train_dataset, self.test_dataset


if __name__ == "__main__":
    cwd = Path(__file__).parent

    dataset = SceneData(cwd / "data/raw/",
                        meta_files_dir=cwd / "data/",
                        valid_scenes=["airport", "street_traffic", "bus", "park"],
                        valid_devices=['a'],
                        target_sample_rate=8000,
                        max_samples_per_scene=10,
                        resize_time=1)

    train, test = dataset.get_datasets()
    assert train.x.shape[0] == train.y.shape[0] == 41360
    assert test.x.shape[0] == test.y.shape[0] == 16240

    assert train.x.shape[1] == test.x.shape[1] == 8000
    assert train.y.shape[1] == test.y.shape[1] == 4

    for key, value in dataset.data.items():
        print(key, value.shape)

    

