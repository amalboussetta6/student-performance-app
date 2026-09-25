from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "student_performance_dataset.csv"


def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    df = df.drop_duplicates().reset_index(drop=True)

    return df