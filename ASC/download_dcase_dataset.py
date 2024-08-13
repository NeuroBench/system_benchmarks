import pyzenodo3
from torchvision.datasets.utils import download_url
import zipfile
import numpy as np
from pathlib import Path
from types import NoneType
from tqdm import tqdm

MKDIR_MODE = 0o2775  # directory permissions


def download_dcase_audio_data(audio_data_path: Path | str | NoneType = None):
    zen = pyzenodo3.Zenodo()

    # DCASE2020 Development and evaluation datasets
    rec = zen.find_record_by_doi("10.5281/zenodo.3819968")

    file_urls = [file["links"]["self"] for file in rec.data["files"]]

    estimated_size = np.sum([file["size"] for file in rec.data["files"]])
    warn_if_size_is_high(estimated_size)

    # Create directory for downloaded zipfiles
    if audio_data_path is None:
        audio_data_path = Path.cwd() / "data"
    elif isinstance(audio_data_path, str):
        audio_data_path = Path(audio_data_path)

    audio_zipped_dir = audio_data_path / "zipped"

    if not audio_zipped_dir.is_dir():
        audio_zipped_dir.mkdir(mode=MKDIR_MODE, parents=True, exist_ok=True)

    # Download
    [download_url(url, audio_zipped_dir, Path(url).parent.name) for url in file_urls]

    # Directory to unzip everything into
    audio_raw_dir = audio_data_path / "raw"

    # Make the directory if it does not exist
    if not audio_raw_dir.is_dir():
        audio_raw_dir.mkdir(mode=MKDIR_MODE, parents=True, exist_ok=True)

    # Get the zipped files
    zip_audio_files = audio_zipped_dir.glob("*.audio.*.zip")
    zip_meta_files = audio_zipped_dir.glob("*.meta.zip")
    unzip_files_in_dir(zip_audio_files, audio_raw_dir)
    unzip_files_in_dir(zip_meta_files, audio_data_path)

    # Delete zip files
    # delete_files_in_directory(audio_zipped_dir)

    return audio_raw_dir


def warn_if_size_is_high(size):
    # Adapted from https://stackoverflow.com/a/59174649
    for order, x in enumerate(['bytes', 'KB', 'MB', 'GB', 'TB']):
        if size < 1024.0:
            if order > 2:
                print(f"Make sure you have enough space to download. Size is {size:3.1f} {x}")
            return f"Size is {size:3.1f} {x}"
        size /= 1024.0


def unzip_files_in_dir(zip_files_list, extract_to_dir):
    for zipfile_ in tqdm(zip_files_list):
        with zipfile.ZipFile(zipfile_, "r") as myzip:
            members = myzip.filelist
            for member in members:
                # So that the wavefiles from all zips are put into one large directory
                member.filename = Path(member.filename).name
                myzip.extract(member, extract_to_dir)


def delete_files_in_directory(directory: Path):
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            delete_files_in_directory(child)
    directory.rmdir()


if __name__ == "__main__":
    main_script_path = Path(__file__).resolve()
    root_dir = main_script_path.parent
    dataset_directory = root_dir / "data"
    download_dcase_audio_data(audio_data_path=dataset_directory)

