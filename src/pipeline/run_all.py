import warnings
from sklearn.exceptions import ConvergenceWarning

from src.config.paths import RAW_DATA

from src.data.load import load_lendingclub, load_fred_macro
from src.data.clean import clean_lendingclub
from src.data.merge_macro import merge_loans_with_macro
from src.data.split import time_based_split

from src.features.build_features import build_features
from src.regimes.regime_labels import assign_macro_regime

from src.models.baseline_pd import train_logistic_pd, evaluate_pd
from src.models.regime_pd import (
    prepare_regime_features,
    train_regime_aware_pd,
    evaluate_pd as evaluate_regime_pd
)


def main():
    # Silence convergence warnings (expected at baseline stage)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    # Load & prepare data
    loans_raw = load_lendingclub(RAW_DATA / "lendingclub.csv")
    loans_clean = clean_lendingclub(loans_raw)

    macro = load_fred_macro(RAW_DATA / "fred_macro.csv")
    loans_macro = merge_loans_with_macro(loans_clean, macro)
    loans_macro = assign_macro_regime(loans_macro, unemployment_threshold=6.0)

    # Time split
    train_df, test_df = time_based_split(
        loans_macro,
        train_end_date="2016-12-31"
    )

    # Features
    X_train, y_train = build_features(train_df)
    X_test, y_test = build_features(test_df)

    # Baseline PD
    baseline_model = train_logistic_pd(X_train, y_train)
    baseline_auc = evaluate_pd(baseline_model, X_test, y_test)

    # Regime-aware PD
    X_train_reg = prepare_regime_features(X_train, train_df["regime"])
    X_test_reg = prepare_regime_features(X_test, test_df["regime"])

    regime_model = train_regime_aware_pd(X_train_reg, y_train)
    regime_auc = evaluate_regime_pd(regime_model, X_test_reg, y_test)

    # Final output only
    print(f"Baseline PD AUC: {baseline_auc:.4f}")
    print(f"Regime-aware PD AUC: {regime_auc:.4f}")


if __name__ == "__main__":
    main()
