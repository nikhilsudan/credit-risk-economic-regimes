import pandas as pd
import numpy as np

from src.config.paths import RAW_DATA
from src.data.load import load_lendingclub, load_fred_macro
from src.data.clean import clean_lendingclub
from src.data.merge_macro import merge_loans_with_macro
from src.regimes.regime_labels import assign_macro_regime
from src.features.build_features import build_features
from src.models.baseline_pd import train_logistic_pd


def main():
    print("\nSTEP 10.1 — Regime Risk Summary\n")

    # -------------------------------------------------
    # Load & prepare data (same logic as Figure 5)
    # -------------------------------------------------
    loans = load_lendingclub(RAW_DATA / "lendingclub.csv")
    loans = clean_lendingclub(loans)

    macro = load_fred_macro(RAW_DATA / "fred_macro.csv")
    loans = merge_loans_with_macro(loans, macro)
    loans = assign_macro_regime(loans)

    # -------------------------------------------------
    # Build features and clean NaNs
    # -------------------------------------------------
    X, y = build_features(loans)
    mask = X.notnull().all(axis=1)

    X_clean = X.loc[mask]
    y_clean = y.loc[mask]
    loans_clean = loans.loc[mask].copy()

    # -------------------------------------------------
    # Train model and predict PDs
    # -------------------------------------------------
    model = train_logistic_pd(X_clean, y_clean)
    loans_clean["pd_hat"] = model.predict_proba(X_clean)[:, 1]

    # -------------------------------------------------
    # Regime-level risk summary
    # -------------------------------------------------
    summary = (
        loans_clean
        .groupby("regime")
        .apply(
            lambda x: pd.Series({
                "Mean PD": x["pd_hat"].mean(),
                "95% PD (Tail Risk)": np.percentile(x["pd_hat"], 95),
                "Observed Default Rate": x["default"].mean(),
                "Sample Size": len(x)
            })
        )
        .round(4)
    )

    print(summary)

    # -------------------------------------------------
    # Relative risk increase
    # -------------------------------------------------
    rel_increase = (
        summary.loc["Stress", "Mean PD"]
        / summary.loc["Expansion", "Mean PD"]
        - 1
    ) * 100

    print(f"\nRelative Mean PD Increase (Stress vs Expansion): {rel_increase:.2f}%")


if __name__ == "__main__":
    main()
