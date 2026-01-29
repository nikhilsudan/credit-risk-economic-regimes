import pandas as pd


def merge_loans_with_macro(
    loans_df: pd.DataFrame,
    macro_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge loan-level data with macroeconomic indicators.

    Parameters
    ----------
    loans_df : pd.DataFrame
        Cleaned LendingClub data with issue_date
    macro_df : pd.DataFrame
        Macro data with date column

    Returns
    -------
    pd.DataFrame
        Loan data enriched with macro variables
    """
    loans_df = loans_df.copy()
    macro_df = macro_df.copy()

    # Ensure datetime
    loans_df["issue_date"] = pd.to_datetime(loans_df["issue_date"])
    macro_df["date"] = pd.to_datetime(macro_df["date"])

    # Align by month
    loans_df["issue_month"] = loans_df["issue_date"].dt.to_period("M").dt.to_timestamp()
    macro_df["month"] = macro_df["date"].dt.to_period("M").dt.to_timestamp()

    merged = loans_df.merge(
        macro_df.drop(columns=["date"]),
        left_on="issue_month",
        right_on="month",
        how="left"
    )

    merged = merged.drop(columns=["issue_month", "month"])

    return merged
