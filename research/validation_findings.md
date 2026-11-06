# Time-Series Momentum — Validation Findings (2016–2020)

## 1. Research Objective

Evaluate the robustness of the original 12-month Time-Series Momentum strategy during the 2016–2020 validation period.

The strategy was developed and analyzed using historical data from 2008–2015.

The purpose of validation is to determine whether the previously observed reduction in portfolio risk and improvement in risk-adjusted performance persist outside the development sample.

The final out-of-sample period (2021–September 2026) remains untouched.

## 2. Methodology

The original strategy specification is maintained without modification.

- Investment universe: SPY, EFA, EEM, AGG, GLD, DBC.
- Momentum lookback: 12 months.
- Signal frequency: Monthly.
- Execution: Next trading session's close.
- Portfolio allocation: 1/6 per ETF with positive momentum.
- Negative momentum signals: Allocation held in remunerated cash.
- Transaction costs: 0.1% of traded notional.
- Cash remuneration: Theoretical DFF-based interest, ACT/360.
- Initial capital: $10,000 per strategy.

The validation period begins on January 4, 2016, and ends on December 31, 2020.

Each portfolio starts with $10,000 and no ETF positions.

Historical observations before 2016 are used to construct the initial momentum signals.

The simulation includes 60 scheduled monthly executions.

## 3. Primary Benchmark Results

| Metric | Momentum | EW Monthly | EW Buy & Hold | SPY Buy & Hold |
|---|---:|---:|---:|---:|
| Final Capital ($) | 11,811.56 | 15,843.42 | 15,741.17 | 20,464.58 |
| CAGR | 3.39% | 9.66% | 9.52% | 15.43% |
| Annual Volatility | 7.09% | 11.38% | 11.77% | 18.85% |
| Maximum Drawdown | -15.75% | -22.98% | -23.19% | -33.72% |
| Sharpe Ratio | 0.342 | 0.766 | 0.733 | 0.795 |
| Calmar Ratio | 0.215 | 0.420 | 0.410 | 0.458 |

### Interpretation

Momentum achieved lower volatility and a smaller maximum drawdown than all three fully invested benchmarks.

However, its absolute returns and risk-adjusted performance were substantially weaker.

In particular:

- Momentum CAGR: 3.39%.
- Equal-Weighted Monthly CAGR: 9.66%.
- Momentum Sharpe ratio: 0.342.
- Equal-Weighted Monthly Sharpe ratio: 0.766.

Therefore, the validation results support a descriptive reduction in portfolio risk but do not support superior risk-adjusted performance.

## 4. Annual Performance

Annual compounded returns, including the initial transaction costs in 2016:

| Year | Momentum | EW Monthly | EW Buy & Hold | SPY Buy & Hold |
|---|---:|---:|---:|---:|
| 2016 | -0.35% | 10.19% | 9.72% | 13.47% |
| 2017 | 14.34% | 17.15% | 17.61% | 21.71% |
| 2018 | -5.44% | -7.57% | -8.34% | -4.57% |
| 2019 | 8.79% | 18.47% | 18.71% | 31.22% |
| 2020 | 0.77% | 12.08% | 12.10% | 18.33% |

Momentum outperformed the two equal-weighted benchmarks in only one of the five years: 2018.

It underperformed SPY Buy & Hold in every calendar year.

The largest annual shortfalls against Equal-Weighted Monthly occurred in 2016, 2019 and 2020.

### Defensive behavior

During 2018, Momentum declined by 5.44%, compared with 7.57% for Equal-Weighted Monthly.

This is consistent with a defensive effect during unfavorable market conditions.

However, the strategy did not consistently outperform during negative market periods, and annual returns alone cannot fully describe intra-year drawdown behavior.

## 5. Cash Exposure Analysis

Average monthly target cash exposure:

| Year | Average Target Cash Weight |
|---|---:|
| 2016 | 47.22% |
| 2017 | 13.89% |
| 2018 | 27.78% |
| 2019 | 50.00% |
| 2020 | 31.94% |

The average target cash allocation during validation was approximately 34.17%.

This corresponds to an average target ETF exposure of approximately 65.83%.

For comparison, average target cash exposure during development was 38.02%.

### Interpretation

Relatively high cash exposure coincided with substantial benchmark underperformance during 2016 and 2019.

During 2017, when the strategy maintained a comparatively low cash allocation, Momentum's returns were closer to those of the diversified benchmarks.

This is consistent with the opportunity cost of holding cash during rising markets.

Nevertheless, cash exposure alone does not fully explain relative performance.

ETF selection, portfolio composition and transaction costs may also contribute.

These exposure statistics describe monthly target allocations rather than realized daily cash weights.

## 6. Comparison with Development

| Momentum Metric | Development (2008–2015) | Validation (2016–2020) |
|---|---:|---:|
| CAGR | 1.86% | 3.39% |
| Annual Volatility | 8.81% | 7.09% |
| Maximum Drawdown | -14.51% | -15.75% |
| Sharpe Ratio | 0.214 | 0.342 |
| Average Target Cash | 38.02% | 34.17% |

Momentum achieved higher standalone CAGR and Sharpe ratio during validation.

However, the primary benchmarks performed considerably better during this period.

The strategy's relative advantage in risk-adjusted performance, observed against certain benchmarks during development, did not persist.

The two periods cover different market environments and have different lengths. Their results should therefore be interpreted descriptively rather than as controlled experiments.

## 7. Exposure-Matched Diagnostic

To investigate whether Momentum's performance is attributable primarily to reduced aggregate exposure or to ETF selection, an additional benchmark is evaluated.

The Exposure-Matched benchmark was originally introduced during development.

Its construction follows three rules:

1. Match Momentum's total monthly target ETF exposure.
2. Allocate that exposure equally across all six ETFs.
3. Invest the remaining capital in theoretical DFF-remunerated cash.

Transaction costs and execution assumptions remain unchanged.

This diagnostic was specified during development but is not treated as a primary benchmark or an independent causal experiment.

### 7.1 Overall Results

| Metric | Momentum | Exposure-Matched |
|---|---:|---:|
| Final Capital ($) | 11,811.56 | 12,831.23 |
| CAGR | 3.39% | 5.12% |
| Annual Volatility | 7.09% | 7.35% |
| Maximum Drawdown | -15.75% | -16.91% |
| Sharpe Ratio | 0.342 | 0.557 |
| Calmar Ratio | 0.215 | 0.303 |

Exposure-Matched achieved a higher CAGR, Sharpe ratio and Calmar ratio.

Momentum maintained slightly lower volatility and a smaller maximum drawdown.

The results therefore suggest that matching Momentum's overall market exposure while diversifying across all ETFs was more effective in terms of returns and risk-adjusted performance during validation.

### 7.2 Annual Comparison

| Year | Momentum | Exposure-Matched |
|---|---:|---:|
| 2016 | -0.35% | 3.40% |
| 2017 | 14.34% | 13.73% |
| 2018 | -5.44% | -2.43% |
| 2019 | 8.79% | 9.18% |
| 2020 | 0.77% | 2.42% |

Momentum outperformed Exposure-Matched in only one of five calendar years: 2017.

The diagnostic benchmark achieved higher annual returns during 2016, 2018, 2019 and 2020.

### 7.3 Interpretation

The results weaken the hypothesis that Momentum's specific ETF-selection mechanism generated a consistent advantage.

During validation, the strategy did not improve aggregate returns or risk-adjusted performance relative to a diversified portfolio with the same total target exposure.

However, this comparison does not establish causality.

Differences in portfolio composition, trading activity and transaction costs remain relevant.

The Exposure-Matched benchmark is useful as an exploratory diagnostic, rather than definitive evidence about the independent contribution of ETF selection.

## 8. Methodological Limitations

Several important limitations remain:

1. The ETF universe was selected retrospectively, potentially introducing selection and survivorship biases.

2. The DFF cash remuneration assumption is theoretical and may not represent an achievable investor return.

3. Trades are modeled using next-session closing prices with proportional transaction costs but without explicit slippage or market impact.

4. Risk metrics rely on standard daily-return annualization conventions.

5. The strategy's lower market exposure makes comparisons with fully invested portfolios imperfectly risk-matched.

6. The observed differences have not been subjected to formal statistical significance testing.

7. Additional diagnostic benchmarks do not establish causal relationships between strategy components and outcomes.

These limitations should be maintained in subsequent analyses.

## 9. Validation Conclusions

The validation period provides mixed evidence.

### Risk reduction

Momentum maintained lower volatility and a smaller maximum drawdown than the primary fully invested benchmarks.

This is consistent with the defensive behavior observed during development.

### Risk-adjusted performance

Momentum failed to outperform the primary benchmarks in terms of Sharpe ratio or Calmar ratio.

Therefore, the hypothesis of superior risk-adjusted performance is not supported by the validation results.

### Exposure and ETF selection

The strategy maintained a substantial allocation to cash.

This likely contributed to its lower risk, but also represented an opportunity cost during favorable market periods.

The Exposure-Matched diagnostic achieved better aggregate returns and risk-adjusted performance, weakening the evidence for additional value from ETF selection.

## 10. Next Steps

The validation analysis is now considered complete.

The following decisions remain unchanged:

- Investment universe.
- Twelve-month momentum signal.
- Monthly signal frequency.
- Next-session execution.
- Allocation rules.
- Transaction-cost assumptions.
- DFF cash remuneration methodology.
- Performance evaluation metrics.

The final evaluation will use the previously reserved 2021–September 2026 period.

No strategy parameters will be optimized using validation or final out-of-sample results.

The final evaluation must report both favorable and unfavorable findings.

## Reproduction

Run from the project root:

    python -m research.validation_analysis

Outputs are saved in:

    research/results/validation/

The exported tables include:

- Primary performance metrics.
- Daily portfolio values.
- Annual strategy returns.
- Annual target cash exposure.
- Exposure-Matched performance metrics.
- Exposure-Matched annual returns.
