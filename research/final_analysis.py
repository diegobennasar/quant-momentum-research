"""Final out-of-sample evaluation: 2021–September 2026.

Run from the project root:
    python -m research.final_analysis

The strategy specification is frozen.
No parameters are optimized using final-period results.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from backtest import (
    INITIAL_CAPITAL,
    TICKERS,
    TRANSACTION_COST_RATE,
    execution_weights,
    target_weights,
    prices,
    simulate_portfolio,
    summarize_strategies,
)


FINAL_START = "2021-01-01"
FINAL_END = "2026-09-30"

RESULTS_DIR = (
    Path(__file__).resolve().parent / "results" / "final"
)


def main():
    # 1. Final-period schedule
    final_schedule = execution_weights.loc[
        FINAL_START:FINAL_END
    ]

    assert len(final_schedule) == 69
    assert final_schedule.index[0] == pd.Timestamp(
        "2021-01-04"
    )

    # First execution uses December 2020 information
    np.testing.assert_allclose(
        final_schedule.iloc[0],
        target_weights.loc["2020-12"].iloc[-1],
    )

    # 2. Time-Series Momentum
    momentum_results = simulate_portfolio(
        execution_weights,
        simulation_start=FINAL_START,
        simulation_end=FINAL_END,
    )

    momentum_values = pd.Series(
        momentum_results["portfolio_history"]
    )

    risk_free_returns = pd.Series(
        momentum_results["risk_free_return_history"]
    )

    # 3. Equal-Weighted Monthly
    ew_schedule = pd.DataFrame(
        1 / len(TICKERS),
        index=execution_weights.index,
        columns=TICKERS,
    )

    ew_results = simulate_portfolio(
        ew_schedule,
        simulation_start=FINAL_START,
        simulation_end=FINAL_END,
    )

    ew_monthly_values = pd.Series(
        ew_results["portfolio_history"]
    )

    # 4. Buy-and-hold benchmarks
    invested_capital = (
        INITIAL_CAPITAL / (1 + TRANSACTION_COST_RATE)
    )

    etf_prices = prices.loc[
        momentum_values.index, TICKERS
    ]

    ew_shares = (
        invested_capital / len(TICKERS)
    ) / etf_prices.iloc[0]

    ew_buyhold_values = (
        etf_prices * ew_shares
    ).sum(axis=1)

    spy_prices = prices.loc[
        momentum_values.index, "SPY"
    ]

    spy_shares = invested_capital / spy_prices.iloc[0]
    spy_values = spy_prices * spy_shares

    # 5. Exposure-Matched diagnostic
    total_exposure = execution_weights.sum(axis=1)

    matched_schedule = pd.DataFrame({
        ticker: total_exposure / len(TICKERS)
        for ticker in TICKERS
    })

    matched_results = simulate_portfolio(
        matched_schedule,
        simulation_start=FINAL_START,
        simulation_end=FINAL_END,
    )

    matched_values = pd.Series(
        matched_results["portfolio_history"]
    )

    # 6. Assemble all portfolios
    strategy_values = {
        "Time-Series Momentum": momentum_values,
        "Equal-Weighted Monthly": ew_monthly_values,
        "Equal-Weighted Buy & Hold": ew_buyhold_values,
        "SPY Buy & Hold": spy_values,
        "Exposure-Matched": matched_values,
    }

    assert all(
        values.index.equals(momentum_values.index)
        for values in strategy_values.values()
    )

    assert risk_free_returns.index.equals(
        momentum_values.index[1:]
    )

    assert momentum_values.index[-1] == pd.Timestamp(
        FINAL_END
    )

    # 7. Performance summary
    summary = summarize_strategies(
        strategy_values,
        risk_free_returns,
    )

    portfolio_paths = pd.DataFrame(strategy_values)

    # 8. Annual compounded returns
    daily_returns = portfolio_paths.pct_change()

    daily_returns.iloc[0] = (
        portfolio_paths.iloc[0] / INITIAL_CAPITAL - 1
    )

    annual_returns = (
        (1 + daily_returns)
        .groupby(daily_returns.index.year)
        .prod() - 1
    ) * 100

    annual_returns.index.name = "Year"

    # 9. Annual target cash exposure
    cash_exposure = 1 - final_schedule.sum(axis=1)

    annual_cash_exposure = (
        cash_exposure
        .groupby(cash_exposure.index.year)
        .mean() * 100
    )

    annual_cash_exposure.index.name = "Year"
    annual_cash_exposure.name = "Average Target Cash (%)"

    # 10. Export results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    summary.to_csv(
        RESULTS_DIR / "performance_summary.csv"
    )

    portfolio_paths.to_csv(
        RESULTS_DIR / "portfolio_values.csv"
    )

    annual_returns.to_csv(
        RESULTS_DIR / "annual_returns_pct.csv"
    )

    annual_cash_exposure.to_csv(
        RESULTS_DIR / "cash_exposure_annual.csv"
    )

    # Final-period research figures
    figures_dir = Path(__file__).resolve().parent.parent / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Portfolio growth
    ax = (portfolio_paths / INITIAL_CAPITAL).plot(
        figsize=(12, 6),
        linewidth=1.5,
    )

    ax.set_title("Final Out-of-Sample: Portfolio Growth")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of $1 Invested")
    ax.axhline(1, color="gray", linestyle="--", alpha=0.5)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(figures_dir / "final_equity_curves.png", dpi=200)
    plt.close()


    # 2. Drawdown curves
    drawdowns = (
        portfolio_paths
        / portfolio_paths.cummax().clip(lower=INITIAL_CAPITAL)
        - 1
    ) * 100

    ax = drawdowns.plot(figsize=(12, 6), linewidth=1.5)

    ax.set_title("Final Out-of-Sample: Drawdowns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(figures_dir / "final_drawdowns.png", dpi=200)
    plt.close()


    # 3. Monthly target cash exposure
    monthly_cash = (1 - final_schedule.sum(axis=1)) * 100

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.step(
        monthly_cash.index,
        monthly_cash.values,
        where="post",
    )

    ax.set_title("Momentum: Target Cash Exposure")
    ax.set_xlabel("Date")
    ax.set_ylabel("Target Cash Weight (%)")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(figures_dir / "final_cash_exposure.png", dpi=200)
    plt.close()

    # 11. Display results
    print(
        f"\nFinal out-of-sample: "
        f"{momentum_values.index[0].date()} "
        f"to {momentum_values.index[-1].date()}"
    )

    print(f"Rebalances: {len(final_schedule)}")

    print("\nStrategy performance:")
    print(summary.round(4).to_string())

    print("\nAnnual returns (%):")
    print(annual_returns.round(2).to_string())

    print("\nAnnual average target cash exposure (%):")
    print(annual_cash_exposure.round(2).to_string())

    print(f"\nSaved results in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
