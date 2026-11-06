# Time-Series Momentum — Final Out-of-Sample Findings

## 1. Research Objective

Evaluate whether the original 12-month Time-Series Momentum strategy maintains its historical downside-risk characteristics and competitive risk-adjusted returns during the final out-of-sample period.

- Development: 2008–2015.
- Validation: 2016–2020.
- Final evaluation: January 2021–September 2026.

The final evaluation uses the original strategy without modifying its parameters or trading assumptions.

Each portfolio starts with $10,000 and no ETF holdings.

## 2. Methodology

The original specification remains unchanged:

- Investment universe: SPY, EFA, EEM, AGG, GLD, DBC.
- Momentum lookback: 12 monthly observations.
- Signal: Positive adjusted-price momentum.
- Rebalancing: Monthly.
- Execution: Following trading session's close.
- Allocation: 1/6 per ETF with positive momentum.
- Negative signals: Theoretical remunerated cash.
- Transaction costs: 0.1% of traded notional.
- Cash remuneration: DFF, ACT/360.

The final period includes 69 scheduled executions, from January 4, 2021, to September 30, 2026.

The first execution uses the December 2020 signal.

The 2026 evaluation ends in September; it does not include a full calendar year.

## 3. Final Performance

| Metric | Momentum | EW Monthly | EW Buy & Hold | SPY | Exposure-Matched |
|---|---:|---:|---:|---:|---:|
| Final Capital ($) | 17,799.80 | 17,948.91 | 18,228.46 | 22,303.67 | 18,051.17 |
| CAGR | 10.58% | 10.74% | 11.04% | 15.01% | 10.85% |
| Annual Volatility | 8.95% | 10.98% | 11.37% | 16.64% | 8.48% |
| Maximum Drawdown | -9.14% | -17.27% | -16.87% | -24.50% | -9.14% |
| Sharpe Ratio | 0.799 | 0.683 | 0.687 | 0.726 | 0.868 |
| Calmar Ratio | 1.157 | 0.622 | 0.654 | 0.613 | 1.187 |

### Interpretation

Momentum achieved similar cumulative returns to the diversified equal-weighted benchmarks while exhibiting lower volatility and a smaller maximum drawdown.

Its Sharpe and Calmar ratios exceeded those of the three primary benchmarks during the final period.

However, SPY Buy & Hold achieved substantially higher absolute returns.

Furthermore, Exposure-Matched achieved higher returns and risk-adjusted performance than Momentum.

## 4. Annual Performance

| Year | Momentum | EW Monthly | EW Buy & Hold | SPY | Exposure-Matched |
|---|---:|---:|---:|---:|---:|
| 2021 | 9.16% | 10.91% | 11.79% | 30.38% | 9.48% |
| 2022 | -1.17% | -8.05% | -6.76% | -18.18% | -1.06% |
| 2023 | 6.56% | 10.89% | 9.32% | 26.18% | 7.49% |
| 2024 | 9.20% | 10.69% | 11.02% | 24.89% | 9.18% |
| 2025 | 24.67% | 26.08% | 26.43% | 17.72% | 24.85% |
| 2026* | 13.73% | 13.73% | 13.98% | 12.71% | 13.73% |

*2026 covers January–September only.*

### Defensive Behavior in 2022

Momentum declined by 1.17% during 2022, compared with losses of 8.05% for Equal-Weighted Monthly and 18.18% for SPY.

This result is consistent with the strategy's dynamic reduction of market exposure.

However, Exposure-Matched also experienced a relatively small decline of 1.06%.

Therefore, the result does not demonstrate that selecting individual positive-momentum ETFs added significant value beyond managing aggregate exposure.

## 5. Cash Exposure

| Year | Average Target Cash |
|---|---:|
| 2021 | 20.83% |
| 2022 | 65.28% |
| 2023 | 45.83% |
| 2024 | 13.89% |
| 2025 | 4.17% |
| 2026* | 0.00% |

The average monthly target cash allocation during the final period was approximately 26.09%.

These figures reflect monthly target allocations, not realized daily cash weights.

High cash exposure during 2022 coincided with comparatively small portfolio losses.

Conversely, the strategy maintained relatively little cash during 2025, allowing greater participation in positive market performance.

## 6. Comparison Across Research Periods

| Momentum Metric | Development | Validation | Final OOS |
|---|---:|---:|---:|
| CAGR | 1.86% | 3.39% | 10.58% |
| Annual Volatility | 8.81% | 7.09% | 8.95% |
| Maximum Drawdown | -14.51% | -15.75% | -9.14% |
| Sharpe Ratio | 0.214 | 0.342 | 0.799 |
| Calmar Ratio | 0.128 | 0.215 | 1.157 |
| Average Target Cash | 38.02% | 34.17% | 26.09% |

### Downside Risk

Momentum exhibited lower annual volatility and a smaller maximum drawdown than all three fully invested primary benchmarks in each evaluation period.

This provides consistent descriptive evidence of historical downside-risk reduction.

### Risk-Adjusted Performance

The results are mixed.

Momentum underperformed the primary benchmarks in Sharpe ratio during validation.

However, its Sharpe ratio exceeded those of the primary benchmarks during the final period.

Consequently, superior risk-adjusted performance cannot be considered a stable characteristic of the strategy.

### ETF Selection vs Aggregate Exposure

Momentum outperformed Exposure-Matched during development.

In contrast, Exposure-Matched achieved superior CAGR and Sharpe ratios during validation and final evaluation.

The evidence therefore does not establish a consistent incremental benefit from selecting individual ETFs beyond the exposure-timing decisions used in the diagnostic benchmark.

Exposure-Matched is not an independent trading signal: its total target ETF exposure is derived from Momentum.

## 7. Methodological Limitations

1. The ETF universe was selected retrospectively, potentially introducing selection and survivorship biases.

2. DFF represents a theoretical cash remuneration proxy rather than an assured investable return.

3. Next-session adjusted closing prices are used as execution proxies without explicit slippage, bid-ask spread or market impact.

4. Primary benchmarks remain fully invested, making them imperfectly matched to Momentum's varying market exposure.

5. Exposure-Matched is a diagnostic comparison and does not establish causality.

6. No formal statistical significance testing has been performed.

7. Each evaluation period starts with a new $10,000 portfolio; results are not a continuous investment history.

8. The study uses simplified annualization conventions and does not model taxes or terminal liquidation costs.

## 8. Final Research Conclusions

The results support three main conclusions.

**First**, the 12-month momentum allocation consistently reduced historical portfolio volatility and maximum drawdown relative to the fully invested primary benchmarks across the three evaluation periods.

**Second**, superior risk-adjusted performance was not consistently observed. Momentum underperformed the primary benchmarks during validation but achieved stronger Sharpe and Calmar ratios during the final out-of-sample period.

**Third**, the Exposure-Matched diagnostic does not establish a persistent incremental benefit from selecting individual positive-momentum ETFs.

The evidence is more consistent with dynamic aggregate exposure playing an important role in the strategy's defensive characteristics.

However, these results remain descriptive and do not establish a causal mechanism or guarantee future performance.

## 9. Overall Assessment

Within the selected six-ETF universe and under the stated assumptions, Time-Series Momentum appears more convincing as a historical risk-management mechanism than as a demonstrated source of persistent risk-adjusted excess returns.

This conclusion is limited by retrospective asset selection, theoretical cash returns, execution assumptions and the absence of formal statistical inference.

No parameters were optimized using the final out-of-sample results.

Future strategy variants should be labeled as new exploratory research rather than retroactive improvements to the original experiment.
