from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.config.paths import RAW_DATA
from src.data.load import load_lendingclub, load_fred_macro
from src.data.clean import clean_lendingclub
from src.data.merge_macro import merge_loans_with_macro
from src.regimes.regime_labels import assign_macro_regime

from src.reporting.style import set_plot_style
from src.reporting.save import save_figure


OUTPUT_DIR = Path("reports/figures")


# ==================================================
# FIGURE 1 — Train / Test timeline (UNCHANGED)
# ==================================================
def plot_train_test_timeline(loans: pd.DataFrame):
    fig, ax = plt.subplots()

    counts = (
        loans
        .set_index("_issue_date_plot")
        .resample("ME")
        .size()
    )

    ax.plot(
        counts.index,
        counts.values,
        color="steelblue",
        linewidth=2
    )

    ax.axvline(
        pd.to_datetime("2016-12-31"),
        color="red",
        linestyle="--",
        label="Train / Test Split"
    )

    ax.set_title("Loan Issuance Over Time (Train/Test Split)")
    ax.set_xlabel("Issue Date")
    ax.set_ylabel("Number of Loans")
    ax.legend()

    save_figure(fig, "figure_1_train_test_split", OUTPUT_DIR)
    plt.close(fig)


# ==================================================
# FIGURE 2 — Unemployment & regimes (UNCHANGED)
# ==================================================
def plot_macro_regimes(macro: pd.DataFrame):
    fig, ax = plt.subplots()

    ax.plot(
        macro["date"],
        macro["unemployment_rate"],
        color="black",
        linewidth=1.5,
        label="Unemployment Rate"
    )

    ax.axhline(
        6.0,
        color="red",
        linestyle="--",
        label="Stress Threshold (6%)"
    )

    ax.fill_between(
        macro["date"],
        macro["unemployment_rate"],
        6.0,
        where=macro["unemployment_rate"] >= 6.0,
        color="red",
        alpha=0.25,
        label="Stress Regime"
    )

    ax.set_title("Macroeconomic Regimes via Unemployment Rate")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unemployment Rate (%)")
    ax.legend()

    save_figure(fig, "figure_2_macro_regimes", OUTPUT_DIR)
    plt.close(fig)


# ==================================================
# FIGURE 3 — Default intensity heatmap (FINAL)
# ==================================================
def plot_default_rate_by_regime(loans: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 4))

    plot_df = loans.dropna(subset=["_issue_date_plot"]).copy()

    heatmap_data = (
        plot_df
        .set_index("_issue_date_plot")
        .groupby("regime")
        .resample("ME")["default"]
        .mean()
        .reset_index()
    )

    pivot = heatmap_data.pivot(
        index="regime",
        columns="_issue_date_plot",
        values="default"
    )

    im = ax.imshow(
        pivot.values,
        aspect="auto",
        cmap="magma",
        interpolation="nearest"
    )

    # Y-axis (regimes)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    # X-axis (years only)
    xticks = range(0, pivot.shape[1], max(1, pivot.shape[1] // 8))
    ax.set_xticks(xticks)
    ax.set_xticklabels(
        [pivot.columns[i].strftime("%Y") for i in xticks],
        rotation=45
    )

    ax.set_title("Default Rate Intensity Over Time by Macroeconomic Regime")
    ax.set_xlabel("Time")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Default Rate")

    save_figure(fig, "figure_3_default_rate_heatmap", OUTPUT_DIR)
    plt.close(fig)


# ==================================================
# MAIN
# ==================================================
def main():
    set_plot_style()

    # Load & prepare data
    loans_raw = load_lendingclub(RAW_DATA / "lendingclub.csv")
    loans_clean = clean_lendingclub(loans_raw)

    macro = load_fred_macro(RAW_DATA / "fred_macro.csv")
    loans_macro = merge_loans_with_macro(loans_clean, macro)
    loans_macro = assign_macro_regime(loans_macro, unemployment_threshold=6.0)

    # --------------------------------------------------
    # Canonical plotting-only issue date (NO GUESSING)
    # --------------------------------------------------
    loans_macro["_issue_date_plot"] = pd.to_datetime(
        loans_macro["issue_d"],
        format="%b-%Y",
        errors="coerce"
    )

    # Generate figures
    plot_train_test_timeline(loans_macro)
    plot_macro_regimes(macro)
    plot_default_rate_by_regime(loans_macro)


if __name__ == "__main__":
    main()
