import pandas as pd


def clean_lendingclub(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean LendingClub data and construct default target.

    Parameters
    ----------
    df : pd.DataFrame
        Raw LendingClub loan-level data

    Returns
    -------
    pd.DataFrame
        Cleaned data with default indicator
    """
    df = df.copy()

    # Keep loans with known outcomes
    df = df[df["loan_status"].isin(["Fully Paid", "Charged Off"])]

    # Binary default target
    df["default"] = (df["loan_status"] == "Charged Off").astype(int)

    # Parse issue date (for time-aware splits)
    df["issue_date"] = pd.to_datetime(df["issue_d"], format="%b-%Y")

    return df
