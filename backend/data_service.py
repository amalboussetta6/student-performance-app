from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BASE_DIR.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "student_performance_dataset_clean.csv"
)


def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    return df