import pandas as pd
from typing import Tuple


def build_features(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Build feature matrix X and target y for PD modeling.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned LendingClub data

    Returns
    -------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Default target
    """
    df = df.copy()

    # Target
    y = df["default"]

    # Select numerical features
    num_features = [
        "loan_amnt",
        "int_rate",
        "annual_inc",
        "dti"
    ]

    # Select categorical features
    cat_features = [
        "grade",
        "term"
    ]

    X_num = df[num_features]
    X_cat = pd.get_dummies(df[cat_features], drop_first=True)

    X = pd.concat([X_num, X_cat], axis=1)

    return X, y
