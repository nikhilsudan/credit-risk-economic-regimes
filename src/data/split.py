import pandas as pd
from typing import Tuple


def time_based_split(
    df: pd.DataFrame,
    train_end_date: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into train/test based on issue_date.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned LendingClub data
    train_end_date : str
        Last date for training data (YYYY-MM-DD)

    Returns
    -------
    train_df, test_df : pd.DataFrame
    """
    df = df.copy()

    train_df = df[df["issue_date"] <= train_end_date]
    test_df = df[df["issue_date"] > train_end_date]

    return train_df, test_df
