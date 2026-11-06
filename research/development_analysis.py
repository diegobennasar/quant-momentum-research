"""Reproduce development-period evidence for Time-Series Momentum (2008-2015).

Run from the repository root:
    python -m research.development_analysis

Uses the existing backtest engine and the frozen local CSV files. This script
never evaluates validation (2016-2020) or final out-of-sample (2021-2026) data.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from backtest import (
    INITIAL_CAPITAL,
    SIMULATION_END,
    SIMULATION_START,
    TICKERS,
    TRANSACTION_COST_RATE,
    execution_weights,
    prices,
    simulate_portfolio,
    summarize_strategies,
)


RESULTS_DIR = Path(__file__).resolve().parent / "results"


def portfolio_series(result):
    """Convert a simulator result into a daily portfolio-value Series."""
    return pd.Series(result["portfolio_history"])


def compounded_returns(returns):
    """Compound returns expressed as decimals across the time index."""
    return (1 + returns).prod() - 1


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Original strategy, risk-free reference, and passive benchmarks.
    momentum_results = simulate_portfolio(execution_weights)
    momentum_values = portfolio_series(momentum_results)
    risk_free_returns = pd.Series(momentum_results["risk_free_return_history"])

    ew_monthly_weights = pd.DataFrame(
        1 / len(TICKERS), index=execution_weights.index, columns=TICKERS
    )
    ew_monthly_values = portfolio_series(simulate_portfolio(ew_monthly_weights))

    # Fixed shares: the initial cost is financed from the $10,000 capital.
    invested_capital = INITIAL_CAPITAL / (1 + TRANSACTION_COST_RATE)
    etf_prices = prices.loc[momentum_values.index, TICKERS]
    ew_shares = (invested_capital / len(TICKERS)) / etf_prices.iloc[0]
    ew_buyhold_values = (etf_prices * ew_shares).sum(axis=1)

    spy_prices = prices.loc[momentum_values.index, "SPY"]
    spy_shares = invested_capital / spy_prices.iloc[0]
    spy_buyhold_values = spy_prices * spy_shares

    primary_values = {
        "Time-Series Momentum": momentum_values,
        "Equal-Weighted Monthly": ew_monthly_values,
        "Equal-Weighted Buy & Hold": ew_buyhold_values,
        "SPY Buy & Hold": spy_buyhold_values,
    }

    # 2. Development-only diagnostic benchmarks.
    constant_weights = pd.DataFrame(
        0.10, index=execution_weights.index, columns=TICKERS
    )
    assert np.allclose(constant_weights.sum(axis=1), 0.60)
    constant_values = portfolio_series(simulate_portfolio(constant_weights))

    invested_fraction = execution_weights.sum(axis=1)
    matched_weights = pd.DataFrame({
        ticker: invested_fraction / len(TICKERS) for ticker in TICKERS
    })
    assert np.allclose(matched_weights.sum(axis=1), invested_fraction)
    matched_values = portfolio_series(simulate_portfolio(matched_weights))

    diagnostic_values = {
        "Constant Exposure 60/40": constant_values,
        "Exposure-Matched": matched_values,
    }

    # All paths must cover precisely the same dates before comparison.
    all_values = {**primary_values, **diagnostic_values}
    assert all(v.index.equals(momentum_values.index) for v in all_values.values())
    assert risk_free_returns.index.equals(momentum_values.index[1:])
    assert momentum_values.index[0] >= pd.Timestamp(SIMULATION_START)
    assert momentum_values.index[-1] <= pd.Timestamp(SIMULATION_END)

    # 3. Overall metrics, consistent with backtest.py and the research report.
    performance_summary = summarize_strategies(all_values, risk_free_returns)
    performance_summary.to_csv(RESULTS_DIR / "performance_summary.csv")

    # 4. Monthly target cash exposure and annual average (not daily drift).
    development_weights = execution_weights.loc[SIMULATION_START:SIMULATION_END]
    cash_exposure = 1 - development_weights.sum(axis=1)
    cash_exposure.name = "Target Cash Weight"
    cash_exposure.to_frame().to_csv(RESULTS_DIR / "cash_exposure_monthly.csv")

    yearly_cash_exposure = cash_exposure.groupby(cash_exposure.index.year).mean() * 100
    yearly_cash_exposure.index.name = "Year"
    yearly_cash_exposure.name = "Average Target Cash (%)"
    yearly_cash_exposure.to_frame().to_csv(RESULTS_DIR / "cash_exposure_annual.csv")

    # 5. Annual returns include first-day entry costs in 2008.
    portfolio_paths = pd.DataFrame(all_values)
    daily_returns = portfolio_paths.pct_change()
    daily_returns.iloc[0] = portfolio_paths.iloc[0] / INITIAL_CAPITAL - 1
    annual_returns = (
        (1 + daily_returns).groupby(daily_returns.index.year).prod() - 1
    )
    annual_returns.index.name = "Year"
    (annual_returns * 100).to_csv(RESULTS_DIR / "annual_returns_pct.csv")

    # 6. Month-end return series and independently recomputable episodes.
    monthly_returns = portfolio_paths.resample("ME").last().pct_change()
    (monthly_returns * 100).to_csv(RESULTS_DIR / "monthly_returns_pct.csv")

    episodes = {
        "Crisis: Sep-Nov 2008": compounded_returns(
            monthly_returns.loc["2008-09":"2008-11"]
        ),
        "Recovery: Mar-Sep 2009": compounded_returns(
            monthly_returns.loc["2009-03":"2009-09"]
        ),
        "Excluding 2008: 2009-2015": compounded_returns(
            annual_returns.loc[2009:2015]
        ),
    }
    episode_summary = pd.DataFrame(episodes).T * 100
    episode_summary.index.name = "Episode"
    episode_summary.to_csv(RESULTS_DIR / "episode_cumulative_returns_pct.csv")

    # 7. Concise and traceable terminal output.
    print("\nDevelopment research: 2008-2015")
    print("\nStrategy performance:")
    print(performance_summary.round(4).to_string())
    print(f"\nAverage target cash weight: {cash_exposure.mean():.2%}")
    print("\nCumulative returns by episode (%):")
    print(episode_summary.round(2).to_string())
    print(f"\nSaved six CSV tables in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()


