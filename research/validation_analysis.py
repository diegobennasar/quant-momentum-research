"""Validation of the frozen 12-month momentum strategy, 2016–2020.

Run from the repository root:
    python -m research.validation_analysis

All portfolios start with $10,000. Strategy rules and performance
metrics remain unchanged from the development period.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from backtest import (
    INITIAL_CAPITAL,
    TICKERS,
    TRANSACTION_COST_RATE,
    execution_weights,
    prices,
    simulate_portfolio,
    summarize_strategies,
    target_weights,
)

VALIDATION_START = "2016-01-01"
VALIDATION_END = "2020-12-31"

RESULTS_DIR = (
    Path(__file__).resolve().parent
    / "results"
    / "validation"
)


def main():
    # 1. Validation schedule and signal timing
    validation_schedule = execution_weights.loc[
        VALIDATION_START:VALIDATION_END
    ]

    assert len(validation_schedule) == 60
    assert validation_schedule.index[0] == pd.Timestamp(
        "2016-01-04"
    )

    np.testing.assert_allclose(
        validation_schedule.iloc[0],
        target_weights.loc["2015-12"].iloc[-1],
    )

    # 2. Original Time-Series Momentum
    momentum_results = simulate_portfolio(
        execution_weights,
        simulation_start=VALIDATION_START,
        simulation_end=VALIDATION_END,
    )

    momentum_values = pd.Series(
        momentum_results["portfolio_history"]
    )

    risk_free_returns = pd.Series(
        momentum_results["risk_free_return_history"]
    )

    # 3. Equal-Weighted Monthly
    equal_weight_schedule = pd.DataFrame(
        1 / len(TICKERS),
        index=execution_weights.index,
        columns=TICKERS,
    )

    monthly_results = simulate_portfolio(
        equal_weight_schedule,
        simulation_start=VALIDATION_START,
        simulation_end=VALIDATION_END,
    )

    monthly_values = pd.Series(
        monthly_results["portfolio_history"]
    )

    # 4. Buy-and-hold benchmarks
    invested_capital = (
        INITIAL_CAPITAL / (1 + TRANSACTION_COST_RATE)
    )

    etf_prices = prices.loc[
        momentum_values.index, TICKERS
    ]

    equal_weight_shares = (
        (invested_capital / len(TICKERS))
        / etf_prices.iloc[0]
    )

    buyhold_values = (
        etf_prices * equal_weight_shares
    ).sum(axis=1)

    spy_prices = prices.loc[
        momentum_values.index, "SPY"
    ]

    spy_shares = invested_capital / spy_prices.iloc[0]
    spy_values = spy_prices * spy_shares

    strategy_values = {
        "Time-Series Momentum": momentum_values,
        "Equal-Weighted Monthly": monthly_values,
        "Equal-Weighted Buy & Hold": buyhold_values,
        "SPY Buy & Hold": spy_values,
    }

    # 5. Consistency checks
    assert all(
        values.index.equals(momentum_values.index)
        for values in strategy_values.values()
    )

    assert risk_free_returns.index.equals(
        momentum_values.index[1:]
    )

    assert momentum_values.index[0] == (
        validation_schedule.index[0]
    )

    assert momentum_values.index[-1] <= pd.Timestamp(
        VALIDATION_END
    )

    entry_cost = momentum_results[
        "transaction_cost_history"
    ][momentum_values.index[0]]

    assert np.isclose(
        momentum_values.iloc[0] + entry_cost,
        INITIAL_CAPITAL,
    )

    assert np.allclose(
        monthly_values.head(),
        buyhold_values.head(),
    )

    # 6. Primary performance summary
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    performance_summary = summarize_strategies(
        strategy_values,
        risk_free_returns,
    )

    performance_summary.to_csv(
        RESULTS_DIR / "performance_summary.csv"
    )

    portfolio_paths = pd.DataFrame(strategy_values)

    portfolio_paths.to_csv(
        RESULTS_DIR / "portfolio_values.csv"
    )

    # 7. Annual compounded returns
    daily_returns = portfolio_paths.pct_change()

    daily_returns.iloc[0] = (
        portfolio_paths.iloc[0] / INITIAL_CAPITAL - 1
    )

    annual_returns = (
        (1 + daily_returns)
        .groupby(daily_returns.index.year)
        .prod() - 1
    )

    annual_returns_pct = annual_returns * 100
    annual_returns_pct.index.name = "Year"

    annual_returns_pct.to_csv(
        RESULTS_DIR / "annual_returns_pct.csv"
    )

    # 8. Annual average target cash exposure
    target_cash = (
        1 - validation_schedule.sum(axis=1)
    )

    annual_cash_exposure = (
        target_cash
        .groupby(target_cash.index.year)
        .mean() * 100
    )

    annual_cash_exposure.index.name = "Year"
    annual_cash_exposure.name = (
        "Average Target Cash (%)"
    )

    annual_cash_exposure.to_csv(
        RESULTS_DIR / "cash_exposure_annual.csv"
    )

    # 9. Exploratory Exposure-Matched benchmark
    # Same total ETF exposure as Momentum,
    # equally distributed across the six ETFs.
    total_etf_exposure = execution_weights.sum(axis=1)

    exposure_matched_schedule = pd.DataFrame({
        ticker: total_etf_exposure / len(TICKERS)
        for ticker in TICKERS
    })

    np.testing.assert_allclose(
        exposure_matched_schedule.sum(axis=1),
        total_etf_exposure,
    )

    matched_results = simulate_portfolio(
        exposure_matched_schedule,
        simulation_start=VALIDATION_START,
        simulation_end=VALIDATION_END,
    )

    matched_values = pd.Series(
        matched_results["portfolio_history"]
    )

    assert matched_values.index.equals(
        momentum_values.index
    )

    diagnostic_values = {
        "Time-Series Momentum": momentum_values,
        "Exposure-Matched": matched_values,
    }

    diagnostic_summary = summarize_strategies(
        diagnostic_values,
        risk_free_returns,
    )

    diagnostic_summary.to_csv(
        RESULTS_DIR / "exposure_matched_summary.csv"
    )

    # 10. Annual returns: Momentum vs Exposure-Matched
    diagnostic_paths = pd.DataFrame(
        diagnostic_values
    )

    diagnostic_daily_returns = (
        diagnostic_paths.pct_change()
    )

    diagnostic_daily_returns.iloc[0] = (
        diagnostic_paths.iloc[0] / INITIAL_CAPITAL - 1
    )

    diagnostic_annual_returns = (
        (1 + diagnostic_daily_returns)
        .groupby(diagnostic_daily_returns.index.year)
        .prod() - 1
    ) * 100

    diagnostic_annual_returns.index.name = "Year"

    diagnostic_annual_returns.to_csv(
        RESULTS_DIR / "exposure_matched_annual_returns_pct.csv"
    )

    # 11. Display results
    print(
        f"\nValidation period: "
        f"{momentum_values.index[0].date()} "
        f"to {momentum_values.index[-1].date()}"
    )

    print(f"Rebalances: {len(validation_schedule)}")

    print("\nPrimary strategies:")
    print(performance_summary.round(4).to_string())

    print("\nAnnual returns (%):")
    print(annual_returns_pct.round(2).to_string())

    print("\nAnnual average target cash exposure (%):")
    print(annual_cash_exposure.round(2).to_string())

    print("\nExploratory Exposure-Matched comparison:")
    print(diagnostic_summary.round(4).to_string())

    print("\nExposure-Matched annual returns (%):")
    print(diagnostic_annual_returns.round(2).to_string())

    print(f"\nSaved validation tables in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
