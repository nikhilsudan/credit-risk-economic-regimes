import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_lendingclub_data(filepath: str) -> pd.DataFrame:
    """
    Load LendingClub loan-level data.
    """
    df = pd.read_csv(filepath, low_memory=False)
    return df


if __name__ == "__main__":
    print("Data download module ready.")
