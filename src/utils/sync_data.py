"""A module to download data repositories to the local folder"""

import json
import os
from typing import Callable

import pandas as pd
import requests
from pyprojroot import here
from loguru import logger


DATA_DIR: str = str(here()) + "/data"


def download_openai_caribbean_dataset():
    logger.info("Downloading OpenAI Caribbean Challenge Dataset")
    base_url: str = "https://raw.githubusercontent.com/drivendataorg/open-ai-caribbean/main/1st%20Place/data"
    train_url: str = base_url + "/train.geojson"
    test_url: str = base_url + "/test.geojson"

    train_response: dict = requests.get(train_url).json()
    test_response: dict = requests.get(test_url).json()

    BASE_DIR: str = f"{DATA_DIR}/openai_caribbean/submission_github_data"
    os.makedirs(BASE_DIR, exist_ok=True)

    with open(BASE_DIR + "/train.json", "w") as f:
        json.dump(train_response, f, indent=4)

    with open(BASE_DIR + "/test.json", "w") as f:
        json.dump(test_response, f, indent=4)

    logger.info(f"OpenAI Caribbean Challenge Dataset saved to {BASE_DIR}")


def download_colobia_meta_demographics():
    logger.info("Downloading Colombia High Density Population Resolution Map")
    data_url: str = "https://data.humdata.org/dataset/2f865527-b7bf-466c-b620-c12b8d07a053/resource/357c91e0-c5fb-4ae2-ad9d-00805e5a075d/download/col_general_2020_csv.zip"
    df = pd.read_csv(data_url)
    BASE_DIR: str = f"{DATA_DIR}/meta_demographics/colombia"
    os.makedirs(BASE_DIR, exist_ok=True)
    df.to_csv(BASE_DIR + "/general_2020.csv", index=False)
    logger.info(f"Colombia High Density Population Dataset saved to {BASE_DIR}")


def main():
    data_callables: list[Callable] = [
        download_openai_caribbean_dataset,
        download_colobia_meta_demographics,
    ]
    logger.debug(f"Found {len(data_callables)} datasets to download")
    for c in data_callables:
        c()


if __name__ == "__main__":
    main()
