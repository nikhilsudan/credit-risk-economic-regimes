import pandas as pd
from pathlib import Path


def load_lendingclub(path: Path) -> pd.DataFrame:
    """
    Load LendingClub loan-level data efficiently.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    usecols = [
        "loan_status",
        "issue_d",
        "loan_amnt",
        "int_rate",
        "annual_inc",
        "dti",
        "grade",
        "term"
    ]

    df = pd.read_csv(
        path,
        usecols=usecols,
        low_memory=False
    )

    print("CSV load complete")
    return df


def load_fred_macro(path: Path) -> pd.DataFrame:
    """
    Load and clean FRED macroeconomic data (robust to schema).
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)

    # Strip whitespace from headers
    df.columns = df.columns.str.strip()

    # Detect date column
    date_col = None
    for c in df.columns:
        if c.lower() in ["date", "observation_date"]:
            date_col = c
            break

    if date_col is None:
        raise ValueError(f"No date column found. Columns: {df.columns.tolist()}")

    # Detect unemployment column
    if "UNRATE" not in df.columns:
        raise ValueError(f"No UNRATE column found. Columns: {df.columns.tolist()}")

    # Standardize names
    df = df.rename(
        columns={
            date_col: "date",
            "UNRATE": "unemployment_rate"
        }
    )

    # Parse datetime
    df["date"] = pd.to_datetime(df["date"])

    return df
