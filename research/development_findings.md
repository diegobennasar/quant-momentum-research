# Time-Series Momentum — Development Research

## 1. Research Objective

Evaluate whether a 12-month Time-Series Momentum strategy improves the risk characteristics and risk-adjusted performance of a diversified ETF portfolio relative to passive investment strategies, after transaction costs.

The primary focus is downside risk, volatility, drawdowns and risk-adjusted returns, rather than maximizing absolute returns.

The general concept relates to Moskowitz, Ooi & Pedersen (2012), [*Time Series Momentum*](https://doi.org/10.1016/j.jfineco.2011.11.003), but this six-ETF cash-sleeve backtest is **not** a replication of their diversified-futures study.

## 2. Strategy Specification

- **Investment universe:** SPY, EFA, EEM, AGG, GLD, DBC
- **Development period:** January 2008 – December 2015
- **Initial capital:** $10,000
- **Momentum signal:** Positive 12-month adjusted-price return
- **Signal frequency:** Monthly, at the final trading session's close
- **Execution:** Next trading session's close
- **Allocation:** 1/6 of portfolio capital per ETF with a positive signal
- **Negative signals:** Corresponding allocation held in cash
- **Transaction costs:** 0.1% of traded notional
- **Cash remuneration:** Theoretical DFF-based daily interest, ACT/360

Historical prices prior to January 2008 are used to calculate the initial momentum signals.

### 2.1. Mathematical and accounting conventions

Let `P[i,t]` denote the adjusted closing price of ETF `i` on the last available session of month `t`. The signal is `M[i,t] = P[i,t] / P[i,t-12] - 1`; only strictly positive signals receive a target weight of `1/6` of total portfolio value. Residual weight is allocated to cash. The signal determined at month-end is traded **at the next session close**, not at the signal close. All positions use fractional share equivalents.

**Transaction costs and self-financing.** If `V-` is portfolio value before a rebalance and `a[i]-` the value of existing ETF holdings, the engine numerically solves for post-cost value `V+` in:

`V+ = V- - 0.001 * sum_i(abs(w[i] * V+ - a[i]-))`.

The simulator applies costs to both buys and sells; no borrowing is intended. No explicit slippage, taxes, financing spread or terminal liquidation charge is modeled.

**Cash interest.** On the interval between successive close valuations, theoretical cash growth is `prod_d(1 + DFF_decimal[d] / 360)`, using every intervening calendar date (including weekends). The DFF series is used retrospectively as a *rate proxy*; the fixing is not an investable retail cash yield and is not necessarily known on the referenced day. See the [New York Fed description](https://www.newyorkfed.org/markets/reference-rates/effr).

**Performance metrics.** CAGR is `(V_end / 10000) ** (365.25 / calendar_days_elapsed) - 1`. Annual volatility is `std(daily_portfolio_returns) * sqrt(252)`; the first daily observation is the initial entry-cost return relative to `$10,000`. The maximum drawdown uses a running peak floored at the initial `$10,000` to include the initial fee. Calmar is `CAGR / abs(maximum_drawdown)`.

**Sharpe convention as implemented.** The reported Sharpe is `sqrt(252) * mean(R_portfolio - R_DFF) / std(R_portfolio - R_DFF)`, where `R_DFF` represents cumulative theoretical DFF interest over the same *close-to-close* period. Because no prior close-to-close DFF return exists on the initial investment date, the entry-cost observation is **excluded from Sharpe**, although it is included in CAGR and volatility. The denominator is the volatility of *excess returns*, not the volatility of portfolio returns. This is a deliberate description of the frozen implementation, not a universal convention; it is a methodological limitation.

The comparison chart normalizes each portfolio's values by the initial `$10,000`, so the first point is slightly below 1 because of entry costs.

## 3. Primary Benchmark Results

| Metric | Momentum | EW Monthly | EW Buy & Hold | SPY Buy & Hold |
|---|---:|---:|---:|---:|
| CAGR | 1.86% | 0.65% | 0.75% | 6.57% |
| Annual volatility | 8.81% | 16.24% | 14.47% | 22.14% |
| Maximum drawdown | -14.51% | -40.89% | -38.97% | -51.92% |
| Sharpe ratio | 0.214 | 0.100 | 0.100 | 0.382 |
| Calmar ratio | 0.128 | 0.016 | 0.019 | 0.127 |

Momentum exhibited substantially lower volatility and maximum drawdown than the fully invested benchmarks. However, its absolute return was limited, and SPY Buy & Hold achieved a considerably higher CAGR.

These results describe the development sample and do not establish out-of-sample effectiveness.

## 4. Exposure Analysis

Momentum maintained an average target allocation of approximately **38.02% in cash**, corresponding to 61.98% invested in ETFs.

Cash exposure was particularly elevated during 2008–2009 and 2015.

Consequently, lower market exposure is a plausible explanation for part of the strategy's reduced volatility.

Two diagnostic benchmarks were constructed:

**Constant Exposure 60/40:** 60% allocated equally across the six ETFs and 40% held in remunerated cash, rebalanced monthly. This is **not** the conventional 60% stocks / 40% bonds portfolio.

**Exposure-Matched:** Uses Momentum's monthly total ETF exposure, but distributes that exposure equally across all six ETFs.

| Metric | Momentum | Constant 60/40 | Exposure-Matched |
|---|---:|---:|---:|
| CAGR | 1.86% | 0.85% | 0.26% |
| Annual volatility | 8.81% | 9.62% | 9.53% |
| Maximum drawdown | -14.51% | -26.22% | -21.18% |
| Sharpe ratio | 0.214 | 0.099 | 0.039 |

Momentum outperformed both diagnostic benchmarks over the development period.

However, these comparisons do not isolate a causal or predictive effect. In particular, the constant 60/40 allocation was chosen after observing Momentum's average exposure, while Exposure-Matched depends directly on Momentum's allocation decisions.

## 5. Crisis Protection and Recovery Lag

### Financial Crisis: September–November 2008

| Strategy | Cumulative return |
|---|---:|
| Momentum | -8.76% |
| Constant 60/40 | -16.09% |
| Equal-Weighted Monthly | -26.18% |

Momentum experienced smaller losses during this episode.

Its target cash allocation increased from 0% in January 2008 to 50% by August, reaching 100% at the November rebalance.

This is consistent with a trend-following mechanism reducing exposure during prolonged market declines.

### Recovery: March–September 2009

| Strategy | Cumulative return |
|---|---:|
| Momentum | +3.11% |
| Constant 60/40 | +20.34% |

Momentum maintained substantial cash exposure during the initial recovery, participating relatively little in rising markets.

This illustrates a potential cost of the 12-month signal: delayed re-entry following market reversals.

## 6. Exposure-Matched Annual Comparison

Momentum outperformed Exposure-Matched in **four of eight years**.

The largest positive annual differences occurred in 2008 and 2013.

During 2009–2015, excluding 2008, cumulative returns were:

- Momentum: +23.82%
- Exposure-Matched: +15.40%

Thus, Momentum's advantage over Exposure-Matched was not exclusively attributable to 2008, although the annual results were inconsistent.

## 7. Methodological Limitations

The following limitations must be acknowledged:

1. **Development-sample evidence:** Findings are exploratory and may not generalize to unseen periods.
2. **Asset selection:** The six-ETF universe was selected retrospectively; survivorship and selection biases have not been fully addressed.
3. **Cash assumptions:** DFF provides a theoretical remuneration proxy, not a guaranteed investable return.
4. **Execution assumptions:** Trades are modeled at next-session closing prices without explicit slippage or market-impact modeling.
5. **Risk estimation:** Annualized volatility and Sharpe ratio use approximate trading-day conventions.
6. **Parameter sensitivity:** Robustness to alternative momentum horizons, transaction costs and allocation rules has not yet been established.
7. **Diagnostic benchmarks:** The 60/40 and Exposure-Matched benchmarks are exploratory tools, not independent validation evidence.
8. **Closing-price execution:** A next-session close is an idealized fill; MOC practical constraints, bid-ask spreads, order-size impact and partial fills are ignored.
9. **Terminal accounting:** Values are marked to market at the final close. An investor actually liquidating the positions would pay additional exit costs.
10. **Return-measure conventions:** First-day fees enter volatility but not Sharpe; variability in calendar days between trading sessions is simplified by `sqrt(252)` annualization.
11. **Time-stamped rates:** The effective DFF fixing may be published only after its reference period. It is an ex-post theoretical benchmark and must not be characterized as a precommitted cash instrument.
12. **Sensitivity:** The choice of development and reporting episodes was analyzed retrospectively. Episode-level comparisons are descriptive rather than independent hypothesis tests.

## 8. Development Conclusions

The 12-month Time-Series Momentum strategy demonstrated meaningful historical downside-risk reduction relative to fully invested ETF portfolios during 2008–2015.

The evidence suggests two relevant mechanisms: reduced aggregate exposure and differences in ETF selection.

However, the strategy also displayed limited absolute returns and substantial underparticipation during the 2009 recovery.

The development results are promising from a risk-management perspective but insufficient to establish a persistent investment advantage.

## 9. Reproduction and Next Steps

Reproduce all the key tables from the frozen inputs by running `python -m research.development_analysis`. This writes six CSV tables under `research/results/`; the original source data stay in `data/`. Run `python -m pytest tests/test_backtest.py -v` for numerical, accounting and timeline checks. Preserve the original input CSVs unchanged and document their sources in `data/README.md`.

- Keep and run the automated tests for signal timing, trading costs, portfolio accounting, cash interest and data integrity.
- Keep the original strategy specification frozen.
- Evaluate the unchanged strategy over the 2016–2020 validation period.
- Preserve 2021–September 2026 for final out-of-sample evaluation.

No strategy modifications should be justified using future validation results without explicitly accounting for the resulting selection bias.