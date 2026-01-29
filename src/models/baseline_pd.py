import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def _mean_impute_numeric(X: pd.DataFrame) -> pd.DataFrame:
    """
    Mean-impute only numeric columns.
    """
    X = X.copy()
    num_cols = X.select_dtypes(include=["number"]).columns
    X[num_cols] = X[num_cols].fillna(X[num_cols].mean())
    return X


def train_logistic_pd(
    X_train: pd.DataFrame,
    y_train: pd.Series
) -> LogisticRegression:
    """
    Train baseline logistic regression PD model.
    """
    X_train = _mean_impute_numeric(X_train)

    model = LogisticRegression(
        max_iter=2000,
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
    Evaluate PD model using ROC-AUC.
    """
    X_test = _mean_impute_numeric(X_test)

    y_prob = model.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, y_prob)

import joblib
from src.config.paths import MODELS_DIR


def load_trained_model():
    """
    Load the previously trained baseline PD model from disk.
    """
    model_path = MODELS_DIR / "baseline_pd_model.joblib"
    return joblib.load(model_path)
