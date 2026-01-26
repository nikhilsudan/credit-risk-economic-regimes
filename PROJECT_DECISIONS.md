PROJECT: Credit Risk Modeling with Economic Regimes

1. Objective
   Build a regime-aware probability-of-default (PD) model for retail credit risk.

2. Dataset
   Lending Club loan-level data with issue dates and loan outcomes.

3. Target Variable
   Binary default indicator.

4. Macroeconomic Data
   Federal Reserve Economic Data (FRED):
   - Unemployment rate
   - Inflation (CPI)
   - Policy interest rate

5. Regime Definition
   Rule-based economic regimes:
   - Expansion
   - Contraction

6. Baseline Model
   Logistic regression (maximum likelihood estimation).

7. Regime Modeling Strategy
   Interaction terms between borrower features and regime indicator.

8. Validation Method
   Time-based train-test split only.

9. Evaluation Metrics
   ROC-AUC
   KS statistic
   Brier score
   Population Stability Index (PSI)
   Characteristic Stability Index (CSI)

10. Stress Testing
    Macroeconomic shock scenarios applied to estimate PD sensitivity.
