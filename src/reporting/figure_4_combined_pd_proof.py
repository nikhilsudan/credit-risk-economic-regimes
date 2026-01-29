from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.config.paths import RAW_DATA
from src.data.load import load_lendingclub, load_fred_macro
from src.data.clean import clean_lendingclub
from src.data.merge_macro import merge_loans_with_macro
from src.regimes.regime_labels import assign_macro_regime
from src.features.build_features import build_features
from src.models.baseline_pd import train_logistic_pd


FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="white", context="paper", font_scale=1.2)


def main():
    # -------------------------
    # Load & prepare data
    # -------------------------
    loans = load_lendingclub(RAW_DATA / "lendingclub.csv")
    loans = clean_lendingclub(loans)

    macro = load_fred_macro(RAW_DATA / "fred_macro.csv")
    loans = merge_loans_with_macro(loans, macro)
    loans = assign_macro_regime(loans)

    X, y = build_features(loans)

    # Drop rows with NaNs for modeling & prediction
    mask = X.notnull().all(axis=1)
    X_clean = X.loc[mask]
    y_clean = y.loc[mask]
    loans_clean = loans.loc[mask].copy()

    model = train_logistic_pd(X_clean, y_clean)
    loans_clean["pd_hat"] = model.predict_proba(X_clean)[:, 1]


    # -------------------------
    # Compute observed defaults
    # -------------------------
    observed = (
        loans_clean.groupby("regime")["default"]
        .mean()
        .to_dict()
    )


    # -------------------------
    # Plot
    # -------------------------
    plt.figure(figsize=(9, 6))

    for regime, color in zip(["Expansion", "Stress"], ["#1f77b4", "#d62728"]):
        subset = loans_clean.loc[loans_clean["regime"] == regime, "pd_hat"]

        sns.kdeplot(
            subset,
            fill=True,
            linewidth=2,
            alpha=0.35,
            label=f"{regime} PD distribution",
            color=color
        )

        plt.axvline(
            observed[regime],
            linestyle="--",
            linewidth=2,
            color=color,
            alpha=0.9,
            label=f"{regime} observed default rate"
        )

    plt.xlabel("Predicted Probability of Default")
    plt.ylabel("Density")

    plt.title(
        "Macroeconomic Regimes, Model-Implied Risk, and Realized Defaults\n"
        "A Unified Credit Risk View"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "figure_5_combined_pd_distribution_and_defaults.png",
        dpi=300
    )
    plt.close()


if __name__ == "__main__":
    main()
