# Credit Risk Modeling Across Macroeconomic Regimes
**A Regime-Dependent Probability of Default Analysis**

---

## 1. Research Question

Traditional credit risk models implicitly assume that the relationship between borrower characteristics and default risk is **stable over time**.

This project asks a more realistic question:

> **Do macroeconomic regimes fundamentally reshape credit risk — not just in level, but in structure?**

Specifically:
- Does the **composition of risk** in a loan portfolio change across regimes?
- Does the **mapping from predicted risk to realized default** remain stable?
- Do key drivers (e.g., interest rates, leverage) exhibit **regime-dependent sensitivities**?

Understanding these effects is critical for:
- Stress testing
- Model validation
- Capital planning
- Risk-based pricing

---

## 2. Methodology

### Data
- Loan-level data (borrower characteristics, loan terms, default outcomes)
- Macroeconomic data (unemployment rate from FRED)
- Sample period aligned to the post-2007 credit cycle

### Regime Definition
Macroeconomic regimes are defined using the unemployment rate:
- **Expansion regime:** unemployment below threshold
- **Stress / contraction regime:** unemployment above threshold

This provides an **economically interpretable and externally observable** regime signal.

### Model
- **Logistic Regression** for Probability of Default (PD)
- Features include:
  - Interest rate
  - Debt-to-income ratio
  - Loan characteristics
  - Credit grades

The model is trained once; analysis focuses on **how its behavior changes across regimes**.

---

## 3. Evidence & Findings

Each figure corresponds to **one explicit claim**.

---

### **Figure 1 — Selection vs Risk Across Regimes (Hero Figure)**

**Claim:**  
**Macroeconomic regimes reshape credit risk even after conditioning on predicted PD.**

**What this shows:**
- **Panel A:** Risk composition shifts across regimes, with stress periods concentrating mass in higher PD deciles
- **Panel B:** For the same predicted PD decile, realized default rates differ by regime

*This indicates regime-dependent calibration drift.*

![Figure 1: Selection vs Risk Across Regimes](reports/figures/figure_5_selection_vs_risk.png)

---

### **Figure 2 — Structural Sensitivity of Default Risk**

**Claim:**  
**The mapping from borrower characteristics to default risk changes across regimes.**

This figure visualizes predicted PD as a nonlinear surface over:
- Interest rate
- Debt-to-income ratio

Differences in slope and curvature across regimes highlight **structural sensitivity shifts**.

![Figure 2: PD Surface by Regime](![alt text](image-1.png))

---

### **Figure 3 — Interest Rate Sensitivity Across Regimes**

**Claim:**  
**Interest rate risk is amplified during economic stress.**

For identical rate increases:
- Predicted PD rises faster in contraction regimes
- The same borrower becomes riskier purely due to macro conditions

![Figure 3: Interest Rate Sensitivity](![alt text](image.png))

---

### **Figure 4 — Model-Implied Risk vs Realized Defaults**

**Claim:**  
**Macroeconomic regimes shift both predicted risk distributions and observed outcomes.**

Predicted PD distributions move rightward during stress periods, while observed default rates remain aligned with model ordering.

This confirms:
- Model ranking stability
- Regime-scaled risk levels

![Figure 4: PD Distribution and Defaults](reports/figures/figure_4_combined_pd_distribution_and_defaults.png)

---

## 4. Key Takeaways

- Credit risk is **regime-dependent**, not regime-invariant
- Selection, calibration, and sensitivity all change across cycles
- Logistic regression remains powerful when paired with:
  - Regime conditioning
  - Structural visualization
  - Economic interpretation

---

## Stress Testing Module (Planned)

Stress testing in this project is currently implemented implicitly via:
- Macroeconomic regime conditioning
- Structural sensitivity analysis
- Counterfactual PD surfaces

This directory is reserved for future extensions such as:
- Explicit scenario-based stress tests
- Regulatory-style capital stress simulations


## 5. Extensions

Potential extensions include:
- Regime-aware recalibration
- Counterfactual stress testing
- Time-varying coefficient models
- Capital allocation applications
