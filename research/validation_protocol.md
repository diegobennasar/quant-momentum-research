# Validation Protocol

## Research Objective

Evaluate whether a 12-month Time-Series Momentum strategy reduces portfolio risk and improves risk-adjusted performance outside its development period.

## Fixed Strategy Specification

- Universe: SPY, EFA, EEM, AGG, GLD, DBC.
- Momentum lookback: 12 months.
- Signal: Positive adjusted-price momentum.
- Signal frequency: Monthly.
- Execution: Next trading session's close.
- Allocation: 1/6 per ETF with positive momentum.
- Negative signals: Theoretical remunerated cash.
- Transaction costs: 0.1% of traded notional.
- Cash remuneration: DFF, ACT/360.
- Initial capital: $10,000.

## Research Periods

- Development: 2008–2015.
- Validation: 2016–2020.
- Final out-of-sample: January 2021–September 2026.

Each period starts with $10,000 and no ETF positions.

Historical data preceding each period are used to construct the initial momentum signals.

## Primary Benchmarks

1. Equal-Weighted Monthly Rebalanced.
2. Equal-Weighted Buy & Hold.
3. SPY Buy & Hold.

## Evaluation Metrics

- CAGR.
- Annualized volatility.
- Maximum drawdown.
- Sharpe ratio.
- Calmar ratio.

## Research Principles

- Keep the original strategy unchanged across evaluation periods.
- Do not optimize parameters using validation or final-period results.
- Report both favorable and unfavorable findings.
- Distinguish exploratory diagnostics from primary benchmarks.
- Document modeling assumptions and limitations.
- Do not interpret historical results as guaranteed future performance.
