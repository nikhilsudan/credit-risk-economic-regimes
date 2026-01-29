import pandas as pd


def assign_macro_regime(
    df: pd.DataFrame,
    unemployment_threshold: float = 6.0
) -> pd.DataFrame:
    """
    Assign macroeconomic regime based on unemployment rate.

    Parameters
    ----------
    df : pd.DataFrame
        Data with unemployment_rate column
    unemployment_threshold : float
        Threshold above which economy is considered stressed

    Returns
    -------
    pd.DataFrame
        Data with 'regime' column
    """
    df = df.copy()

    df["regime"] = (
        df["unemployment_rate"] > unemployment_threshold
    ).map({True: "Stress", False: "Expansion"})

    return df
