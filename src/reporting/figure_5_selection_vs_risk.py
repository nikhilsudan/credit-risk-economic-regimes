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


# -------------------------------------------------
# Style (journal / research)
# -------------------------------------------------
sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)

FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # -------------------------------------------------
    # Load & prepare data
    # -------------------------------------------------
    loans = load_lendingclub(RAW_DATA / "lendingclub.csv")
    loans = clean_lendingclub(loans)

    macro = load_fred_macro(RAW_DATA / "fred_macro.csv")
    loans = merge_loans_with_macro(loans, macro)
    loans = assign_macro_regime(loans)

    # -------------------------------------------------
    # Build ML features & train logistic regression
    # -------------------------------------------------
    X, y = build_features(loans)
    mask = X.notnull().all(axis=1)

    loans = loans.loc[mask].copy()
    X = X.loc[mask]
    y = y.loc[mask]

    model = train_logistic_pd(X, y)
    loans["pd_hat"] = model.predict_proba(X)[:, 1]

    # -------------------------------------------------
    # Create PD deciles (risk buckets)
    # -------------------------------------------------
    loans["pd_decile"] = pd.qcut(
        loans["pd_hat"],
        q=10,
        labels=False
    ) + 1  # 1 = lowest risk, 10 = highest risk

    # -------------------------------------------------
    # PANEL A: Portfolio risk composition
    # -------------------------------------------------
    composition = (
    loans
    .groupby(["regime", "pd_decile"], as_index=False)
    .size()
)

    composition["share"] = (
    composition
    .groupby("regime")["size"]
    .transform(lambda x: x / x.sum())
)

    # -------------------------------------------------
    # PANEL B: Conditional default rates
    # -------------------------------------------------
    default_by_risk = (
        loans
        .groupby(["regime", "pd_decile"])["default"]
        .mean()
        .reset_index()
    )

    # -------------------------------------------------
    # Plot (2-panel hero figure)
    # -------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

    # ----- Panel A
    sns.lineplot(
        data=composition,
        x="pd_decile",
        y="share",
        hue="regime",
        marker="o",
        ax=axes[0]
    )

    axes[0].set_title(
        "A. Risk Composition Shift Across Regimes\n"
        "(Logistic Regression PD Deciles)"
    )
    axes[0].set_xlabel("Predicted PD Decile (1 = Low Risk, 10 = High Risk)")
    axes[0].set_ylabel("Share of Loan Portfolio")
    axes[0].legend(title="Regime")

    # ----- Panel B
    sns.lineplot(
        data=default_by_risk,
        x="pd_decile",
        y="default",
        hue="regime",
        marker="o",
        ax=axes[1]
    )

    axes[1].set_title(
        "B. Default Rates Conditional on Predicted Risk\n"
        "(Model Calibration by Regime)"
    )
    axes[1].set_xlabel("Predicted PD Decile")
    axes[1].set_ylabel("Observed Default Rate")
    axes[1].legend(title="Regime")

    plt.suptitle(
        "Selection vs Risk: How Economic Regimes Reshape Credit Outcomes\n"
        "Logistic Regression–Based Probability of Default Analysis",
        y=1.05
    )

    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "figure_12_hero_selection_vs_risk.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


if __name__ == "__main__":
    main()
