import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def _mean_impute_numeric(X: pd.DataFrame) -> pd.DataFrame:
    """
    Mean-impute numeric columns only.
    """
    X = X.copy()
    num_cols = X.select_dtypes(include=["number"]).columns
    X[num_cols] = X[num_cols].fillna(X[num_cols].mean())
    return X


def prepare_regime_features(
    X: pd.DataFrame,
    regime: pd.Series
) -> pd.DataFrame:
    """
    Add regime dummy and interaction terms.
    """
    X_reg = X.copy()

    # Regime indicator: 1 = Stress, 0 = Expansion
    X_reg["regime_stress"] = (regime == "Stress").astype(int)

    # Interaction terms
    for col in X.columns:
        X_reg[f"{col}_x_stress"] = X[col] * X_reg["regime_stress"]

    return X_reg


def train_regime_aware_pd(
    X_train: pd.DataFrame,
    y_train: pd.Series
) -> LogisticRegression:
    """
    Train regime-aware PD model with numeric imputation.
    """
    X_train = _mean_impute_numeric(X_train)

    model = LogisticRegression(
        max_iter=3000,
        solver="lbfgs"
    )

    model.fit(X_train, y_train)
    return model


def evaluate_pd(
    model: LogisticRegression,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> float:
    """
    Evaluate regime-aware PD using ROC-AUC.
    """
    X_test = _mean_impute_numeric(X_test)

    prob = model.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, prob)
