"""Time-series momentum research | development period: 2008-2015.

All portfolios start with $10,000 at their first scheduled execution.
Historical ETF data prior to 2008 are used only to construct momentum signals.
The validation period (2016-2020) is deliberately not evaluated here.

Requires the frozen local files data/etf_prices.csv and data/dff_rates.csv.
Importing this module loads data and builds schedules but does not run a backtest.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# 1. Research configuration
TICKERS = ["SPY", "EFA", "EEM", "AGG", "GLD", "DBC"]
SIMULATION_START = "2008-01-01"
SIMULATION_END = "2015-12-31"
INITIAL_CAPITAL = 10_000.0
TRANSACTION_COST_RATE = 0.001
PROJECT_ROOT = Path(__file__).resolve().parent


# 2. Local market data and cash rates
prices = pd.read_csv(
    PROJECT_ROOT / "data" / "etf_prices.csv", index_col=0, parse_dates=True
)
prices = prices.reindex(columns=TICKERS)
assert not prices.empty, "No ETF prices loaded"
assert prices.index.is_unique and prices.index.is_monotonic_increasing
assert not prices.isna().any().any(), "Missing ETF prices"
assert np.isfinite(prices.to_numpy()).all() and (prices > 0).all().all()
daily_asset_returns = prices.pct_change(fill_method=None)

# DFF rates were saved as annual decimals (e.g., 0.04 means 4%).
annual_cash_rates = pd.read_csv(
    PROJECT_ROOT / "data" / "dff_rates.csv", index_col=0, parse_dates=True
)["DFF"]
assert annual_cash_rates.index.is_unique and annual_cash_rates.index.is_monotonic_increasing


# 3. Twelve-month momentum and next-session execution
monthly_prices = prices.groupby(prices.index.to_period("M")).tail(1)
momentum_12m = monthly_prices.pct_change(periods=12, fill_method=None).dropna()
signals = (momentum_12m > 0).astype(int)
target_weights = signals / len(TICKERS)

cash_weights = 1 - target_weights.sum(axis=1)
assert (target_weights >= 0).all().all()
assert (cash_weights >= -1e-12).all()

signal_dates = target_weights.index
trading_dates = prices.index
execution_positions = trading_dates.searchsorted(signal_dates, side="right")
valid_executions = execution_positions < len(trading_dates)
execution_dates = trading_dates[execution_positions[valid_executions]]

execution_weights = target_weights.loc[signal_dates[valid_executions]].copy()
execution_weights.index = execution_dates
assert (execution_dates > signal_dates[valid_executions]).all()


# 4. Transaction-cost solver and reusable portfolio simulator
def solve_post_cost_value(
    portfolio_value, asset_values, target_weights, cost_rate,
    tolerance=1e-10, max_iterations=100
):
    """Solve the self-financing portfolio value after proportional trading costs."""
    estimate = portfolio_value
    for _ in range(max_iterations):
        target_asset_values = target_weights * estimate
        total_traded_notional = (target_asset_values - asset_values).abs().sum()
        new_estimate = portfolio_value - cost_rate * total_traded_notional
        if abs(new_estimate - estimate) < tolerance:
            return new_estimate
        estimate = new_estimate
    raise RuntimeError("Fixed-point iteration did not converge")


def simulate_portfolio(
        weight_schedule,
        simulation_start=SIMULATION_START,
        simulation_end=SIMULATION_END,
):
    """Simulate daily ETF holdings, theoretical cash interest, and trades.

    Every call begins with INITIAL_CAPITAL in cash and no ETF positions.
    Optional dates allow a later, separate validation without changing rules.
    """
    # The research specification is long-only and unleveraged; reject invalid
    # schedules instead of silently financing a leveraged portfolio with cash.
    if not weight_schedule.columns.equals(prices.columns):
        raise ValueError("Weight columns must match ETF price columns and order")
    if not weight_schedule.index.is_unique or not weight_schedule.index.is_monotonic_increasing:
        raise ValueError("Weight schedule dates must be unique and sorted")
    if weight_schedule.isna().any().any() or not np.isfinite(weight_schedule.to_numpy()).all():
        raise ValueError("Weight schedule contains missing or non-finite weights")
    if (weight_schedule < -1e-12).any().any() or (weight_schedule.sum(axis=1) > 1 + 1e-12).any():
        raise ValueError("Weights must be nonnegative and sum to at most 1")
    if pd.Timestamp(simulation_end) > prices.index[-1]:
        raise ValueError("Simulation end exceeds the available ETF price history")

    simulation_weights = weight_schedule.loc[simulation_start:simulation_end]
    if simulation_weights.empty:
        raise ValueError("No scheduled trades in the simulation period")

    first_execution_date = simulation_weights.index[0]
    asset_values = pd.Series(0.0, index=prices.columns)
    cash_value = INITIAL_CAPITAL
    previous_date = None

    portfolio_history = {}
    trade_history = {}
    transaction_cost_history = {}
    cash_interest_history = {}
    risk_free_return_history = {}

    for date in prices.loc[first_execution_date:simulation_end].index:
        if previous_date is not None:
            # Interest accrues on all calendar days, including weekends.
            period_rates = annual_cash_rates.loc[
                previous_date : date - pd.Timedelta(days=1)
            ]
            assert len(period_rates) == (date - previous_date).days
            assert period_rates.notna().all(), "Missing DFF rate"
            cash_growth_factor = (1 + period_rates / 360).prod()
            risk_free_return_history[date] = cash_growth_factor - 1

            cash_before_interest = cash_value
            cash_value *= cash_growth_factor
            cash_interest_history[date] = cash_value - cash_before_interest
            asset_values = asset_values * (1 + daily_asset_returns.loc[date])

        portfolio_value = asset_values.sum() + cash_value

        # Execute the previously observed month-end signal at this session's close.
        if date in simulation_weights.index:
            desired_weights = simulation_weights.loc[date]
            post_cost_value = solve_post_cost_value(
                portfolio_value, asset_values, desired_weights,
                TRANSACTION_COST_RATE,
            )
            target_asset_values = desired_weights * post_cost_value
            trade_values = target_asset_values - asset_values
            transaction_cost = TRANSACTION_COST_RATE * trade_values.abs().sum()

            assert np.isclose(portfolio_value - post_cost_value, transaction_cost)
            trade_history[date] = trade_values.copy()
            transaction_cost_history[date] = transaction_cost
        
            asset_values = target_asset_values
            cash_value = post_cost_value - asset_values.sum()
            portfolio_value = post_cost_value
            assert np.allclose(asset_values / portfolio_value, desired_weights)

        portfolio_history[date] = portfolio_value
        previous_date = date

    return {
        "portfolio_history": portfolio_history,
        "trade_history": trade_history,
        "transaction_cost_history": transaction_cost_history,
        "cash_interest_history": cash_interest_history,
        "risk_free_return_history": risk_free_return_history,
    }


# 5. Reusable performance evaluation
def calculate_performance_metrics(portfolio_values, risk_free_returns, initial_capital):
    """Calculate performance metrics, including initial entry costs in CAGR and volatility.

    The first-day commission is excluded from Sharpe because the first
    observation has no matching close-to-close risk-free return.
    """
    elapsed_years = (portfolio_values.index[-1] - portfolio_values.index[0]).days / 365.25
    cagr = (portfolio_values.iloc[-1] / initial_capital) ** (1 / elapsed_years) - 1

    daily_returns = portfolio_values.pct_change()
    daily_returns.iloc[0] = portfolio_values.iloc[0] / initial_capital - 1
    annual_volatility = np.sqrt(252) * daily_returns.std()

    running_max = portfolio_values.cummax().clip(lower=initial_capital)
    max_drawdown = (portfolio_values / running_max - 1).min()
    calmar_ratio = cagr / abs(max_drawdown) if max_drawdown < 0 else np.nan

    excess_returns = daily_returns.loc[risk_free_returns.index] - risk_free_returns
    excess_volatility = excess_returns.std()
    sharpe_ratio = (
        np.sqrt(252) * excess_returns.mean() / excess_volatility
        if excess_volatility > 0 else np.nan
    )
    return {
        "CAGR": cagr,
        "Annual Volatility": annual_volatility,
        "Maximum Drawdown": max_drawdown,
        "Calmar Ratio": calmar_ratio,
        "Sharpe Ratio": sharpe_ratio,
    }


def summarize_strategies(strategy_values, risk_free_returns):
    """Build a consistent comparison for any dictionary of portfolio paths."""
    summary = pd.DataFrame({
        name: calculate_performance_metrics(values, risk_free_returns, INITIAL_CAPITAL)
        for name, values in strategy_values.items()
    }).T
    summary.insert(
        0, "Final Capital ($)",
        pd.Series({name: values.iloc[-1] for name, values in strategy_values.items()}),
    )
    return summary


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # 6. Development: Momentum and three independent benchmarks
    momentum_results = simulate_portfolio(execution_weights)
    portfolio_values = pd.Series(momentum_results["portfolio_history"])
    risk_free_returns = pd.Series(momentum_results["risk_free_return_history"])

    ew_monthly_target_weights = pd.DataFrame(
        1 / len(TICKERS), index=execution_weights.index, columns=TICKERS
    )
    ew_monthly_results = simulate_portfolio(ew_monthly_target_weights)
    ew_monthly_portfolio_values = pd.Series(ew_monthly_results["portfolio_history"])

    invested_capital = INITIAL_CAPITAL / (1 + TRANSACTION_COST_RATE)
    ew_prices = prices.loc[portfolio_values.index, TICKERS]
    ew_shares = (invested_capital / len(TICKERS)) / ew_prices.iloc[0]
    ew_portfolio_values = (ew_prices * ew_shares).sum(axis=1)

    spy_prices = prices.loc[portfolio_values.index, "SPY"]
    spy_shares = invested_capital / spy_prices.iloc[0]
    spy_portfolio_values = spy_shares * spy_prices

    strategy_values = {
        "Time-Series Momentum": portfolio_values,
        "Equal-Weighted Monthly": ew_monthly_portfolio_values,
        "Equal-Weighted Buy & Hold": ew_portfolio_values,
        "SPY Buy & Hold": spy_portfolio_values,
    }
    performance_summary = summarize_strategies(strategy_values, risk_free_returns)


    # 7. Permanent checks and development outputs
    assert all(
        values.index.equals(portfolio_values.index)
        for values in strategy_values.values()
    )
    assert risk_free_returns.index.equals(portfolio_values.index[1:])
    assert portfolio_values.index[0] >= pd.Timestamp(SIMULATION_START)
    assert portfolio_values.index[-1] <= pd.Timestamp(SIMULATION_END)
    assert np.isclose(
        portfolio_values.iloc[0]
        + momentum_results["transaction_cost_history"][portfolio_values.index[0]],
        INITIAL_CAPITAL,
    )
    assert np.allclose(ew_monthly_portfolio_values.head(), ew_portfolio_values.head())

    print(f"\nDevelopment: {portfolio_values.index[0].date()} to {portfolio_values.index[-1].date()}")
    print("\nPrimary strategies:")
    print(performance_summary.round(4).to_string())
    
    comparison_values = pd.DataFrame(strategy_values) / INITIAL_CAPITAL
    comparison_values.plot(figsize=(12, 6))
    plt.title("Portfolio Performance Comparison (2008–2015)")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1 Invested")
    plt.axhline(y=1, color="gray", linestyle="--", linewidth=1, alpha=0.6)
    figures_dir = PROJECT_ROOT / "figures"
    figures_dir.mkdir(exist_ok=True)
    plt.savefig(figures_dir / "portfolio_comparison.png", dpi=300, bbox_inches="tight")
    plt.show()