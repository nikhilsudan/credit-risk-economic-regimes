# Project Design Decisions

This document records key modeling and design choices made during the
development of the regime-dependent credit risk model, along with
their rationale and trade-offs.

## Macroeconomic Regime Definition

Macroeconomic regimes are defined using the unemployment rate
sourced from FRED.

- Expansion regime: unemployment below threshold
- Stress (contraction) regime: unemployment above threshold

Rationale:
- Observable, externally verifiable macro signal
- Direct economic interpretation
- Avoids latent regime overfitting

## Model Choice

Logistic regression was selected for PD estimation due to:
- Interpretability of coefficients
- Alignment with industry credit risk practice
- Compatibility with regime comparison

The goal is not maximum predictive power, but structural analysis
of risk behavior across regimes.

## Stress Modeling Approach

No standalone stress model was implemented.

Instead, stress is represented via:
- Regime conditioning
- Regime-specific distributions
- Regime-conditional sensitivities

This mirrors industry stress-testing workflows where the same model
is evaluated under different macroeconomic states.

## Scope and Limitations

This project focuses on:
- Structural differences in credit risk across regimes

It does not attempt:
- Full CCAR-style stress testing
- Regulatory capital estimation
- Production-grade deployment
