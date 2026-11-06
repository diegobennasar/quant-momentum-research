# Research Summary — Time-Series Momentum Across Six ETFs

## Question

Does a 12-month monthly time-series momentum allocation reduce downside risk and improve risk-adjusted outcomes relative to passive six-ETF benchmarks?

## Design

Six ETFs (SPY, EFA, EEM, AGG, GLD and DBC); 12-month adjusted-price momentum; 1/6 allocation per positive-signal ETF; remaining capital in theoretical DFF-remunerated cash; next-session closing-price execution; 0.1% traded-notional fee.

Each sample restarts from $10,000.

The strategy was specified and investigated in 2008–2015, checked unchanged in 2016–2020, and assessed in the reserved 2021–September 2026 final period.

## Principal Findings

| Metric | Development 2008–15 | Validation 2016–20 | Final 2021–Sep 2026 |
|---|---:|---:|---:|
| Momentum CAGR | 1.86% | 3.39% | 10.58% |
| Momentum Sharpe | 0.214 | 0.342 | 0.799 |
| Momentum maximum drawdown | -14.51% | -15.75% | -9.14% |
| Equal-Weighted Monthly maximum drawdown | -40.89% | -22.98% | -17.27% |
| Momentum target cash mean | 38.02% | 34.17% | 26.09% |

- **Risk:** Momentum had less realized volatility and a smaller maximum drawdown than all three fully invested primary benchmarks in every period.

- **Risk-adjusted returns:** Improvement was not consistent. Momentum lagged all primary benchmarks in validation on Sharpe and Calmar, but exceeded them in the final period.

- **Exposure:** The dynamic cash weight plausibly explains an important share of the observed protection, particularly in 2022.

- **Selection:** The exposure-matched control had better CAGR and Sharpe than Momentum in validation and the final period. This undermines a claim of consistently beneficial ETF selection, but does not constitute a causal decomposition.

## Interpretation

The evidence better supports time-series momentum as a **historically defensive exposure-management mechanism** in this particular ETF portfolio than as a demonstrated source of stable risk-adjusted excess returns or ETF-selection alpha.

These are descriptive backtest results, not statistically established causal effects or an investable performance record.

## Important Limitations

Retrospective universe choice, theoretical DFF cash yield, closing-price execution without slippage, unequal market exposure relative to fully invested comparators, short and heterogeneous samples, no formal inference and reinitialized capital across periods.

The year 2026 ends on September 30.

## Files

- `research/development_findings.md`: exploratory findings and diagnostics.
- `research/validation_findings.md`: validation and exposure-matched comparison.
- `research/final_findings.md`: final-period analysis and full methodology caveats.
- `research/validation_protocol.md`: original research rules set before the final period was inspected.
