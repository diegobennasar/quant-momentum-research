import numpy as np
import pandas as pd
import backtest as bt

from backtest import (
    solve_post_cost_value,
    prices,
    target_weights,
    execution_weights,
    SIMULATION_START,
    SIMULATION_END,
    simulate_portfolio,
    annual_cash_rates,
    INITIAL_CAPITAL,
)


def test_initial_transaction_cost():
    initial_capital = 10_000.0
    cost_rate = 0.001

    tickers = ["SPY", "EFA", "EEM", "AGG", "GLD", "DBC"]

    asset_values = pd.Series(0.0, index=tickers)
    target_weights = pd.Series(1 / len(tickers), index=tickers)

    post_cost_value = solve_post_cost_value(
        initial_capital,
        asset_values,
        target_weights,
        cost_rate,
    )

    transaction_cost = cost_rate * post_cost_value

    assert np.isclose(
        post_cost_value + transaction_cost,
        initial_capital,
    )


def test_rebalancing_with_buy_and_sell():
    portfolio_value = 10_000.0
    cost_rate = 0.001

    asset_values = pd.Series({
        "SPY": 6_000.0,
        "AGG": 0.0,
    })

    target_weights = pd.Series({
        "SPY": 0.30,
        "AGG": 0.30,
    })

    post_cost_value = solve_post_cost_value(
        portfolio_value,
        asset_values,
        target_weights,
        cost_rate,
    )

    target_asset_values = target_weights * post_cost_value
    trades = target_asset_values - asset_values

    transaction_cost = cost_rate * trades.abs().sum()

    assert trades["SPY"] < 0
    assert trades["AGG"] > 0

    assert np.isclose(post_cost_value, 9_994.0)

    assert np.isclose(
        portfolio_value,
        post_cost_value + transaction_cost,
    )


def test_signal_execution_dates():
    development_executions = execution_weights.loc[
        SIMULATION_START:SIMULATION_END
    ]

    assert len(development_executions) == 96

    for execution_date, executed_weights in development_executions.iterrows():

        position = prices.index.get_loc(execution_date)
        previous_trading_date = prices.index[position - 1]

        assert previous_trading_date in target_weights.index

        expected_weights = target_weights.loc[previous_trading_date]

        np.testing.assert_allclose(
            executed_weights,
            expected_weights
        )


def test_cash_interest_calculation():
    results = simulate_portfolio(execution_weights)

    portfolio_values = pd.Series(results["portfolio_history"])
    cash_interests = pd.Series(results["cash_interest_history"])

    # First date with positive cash interest
    first_interest_date = cash_interests[
        cash_interests > 1e-8
    ].index[0]

    # Most recent rebalance before receiving interest
    previous_rebalance = execution_weights.index[
        execution_weights.index < first_interest_date
    ][-1]

    # Cash held immediately after that rebalance
    initial_cash = (
        portfolio_values.loc[previous_rebalance]
        * (1 - execution_weights.loc[previous_rebalance].sum())
    )

    # Historical DFF rates for the interest-accrual period
    period_rates = annual_cash_rates.loc[
        previous_rebalance:
        first_interest_date - pd.Timedelta(days=1)
    ]

    expected_interest = initial_cash * (
        (1 + period_rates / 360).prod() - 1
    )

    recorded_interest = cash_interests.loc[first_interest_date]

    np.testing.assert_allclose(
        recorded_interest,
        expected_interest,
        rtol=0,
        atol=1e-9,
    )


def test_development_data_integrity():
    development_prices = prices.loc[
        SIMULATION_START:SIMULATION_END
    ]

    # Check ETF price data
    assert not development_prices.empty
    assert development_prices.index.is_monotonic_increasing
    assert development_prices.index.is_unique
    assert development_prices.notna().all().all()

    # Check daily DFF coverage
    first_date = development_prices.index[0]
    last_date = development_prices.index[-1]

    calendar_dates = pd.date_range(
        first_date,
        last_date - pd.Timedelta(days=1),
        freq="D"
    )

    development_rates = annual_cash_rates.reindex(calendar_dates)

    assert annual_cash_rates.index.is_unique
    assert development_rates.notna().all()


def test_cash_interest_over_weekend(monkeypatch):
    dates = pd.to_datetime(["2020-01-03", "2020-01-06"])

    synthetic_prices = pd.DataFrame(
        100.0, index=dates, columns=bt.TICKERS
    )

    synthetic_rates = pd.Series(
        0.036,
        index=pd.date_range("2020-01-03", periods=3)
    )

    monkeypatch.setattr(bt, "prices", synthetic_prices)
    monkeypatch.setattr(
        bt,
        "daily_asset_returns",
        synthetic_prices.pct_change(fill_method=None)
    )
    monkeypatch.setattr(bt, "annual_cash_rates", synthetic_rates)

    weights = pd.DataFrame(
        0.0, index=[dates[0]], columns=bt.TICKERS
    )

    results = bt.simulate_portfolio(
        weights,
        simulation_start="2020-01-03",
        simulation_end="2020-01-06"
    )

    expected_value = bt.INITIAL_CAPITAL * (1 + 0.036 / 360) ** 3
    actual_value = results["portfolio_history"][dates[1]]

    np.testing.assert_allclose(
        actual_value, expected_value, rtol=0, atol=1e-9
    )

def test_momentum_signal_uses_exactly_twelve_months():
    """Check the signal formula against hand-indexed month-end prices."""
    for signal_date in (pd.Timestamp("2007-12-31"), pd.Timestamp("2015-12-31")):
        signal_position = bt.monthly_prices.index.get_loc(signal_date)
        previous_prices = bt.monthly_prices.iloc[signal_position - 12]
        current_prices = bt.monthly_prices.loc[signal_date]
        expected = (current_prices > previous_prices).astype(int) / len(bt.TICKERS)

        np.testing.assert_allclose(
            bt.target_weights.loc[signal_date].to_numpy(),
            expected.to_numpy(),
            rtol=0,
            atol=1e-12,
        )


def test_synthetic_partial_investment_and_price_gain(monkeypatch):
    """A known 10% ETF gain must affect exactly the invested fraction."""
    dates = pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"])
    synthetic_prices = pd.DataFrame(100.0, index=dates, columns=bt.TICKERS)
    synthetic_prices.loc[dates[1]:, "SPY"] = 110.0

    synthetic_rates = pd.Series(
        0.0, index=pd.date_range("2020-01-02", "2020-01-05", freq="D")
    )
    monkeypatch.setattr(bt, "prices", synthetic_prices)
    monkeypatch.setattr(
        bt, "daily_asset_returns", synthetic_prices.pct_change(fill_method=None)
    )
    monkeypatch.setattr(bt, "annual_cash_rates", synthetic_rates)

    weights = pd.DataFrame(0.0, index=[dates[0]], columns=bt.TICKERS)
    weights.loc[dates[0], "SPY"] = 0.5

    result = bt.simulate_portfolio(
        weights, simulation_start="2020-01-02", simulation_end="2020-01-06"
    )
    expected_after_cost = bt.INITIAL_CAPITAL / (1 + bt.TRANSACTION_COST_RATE * 0.5)

    np.testing.assert_allclose(result["portfolio_history"][dates[0]], expected_after_cost)
    np.testing.assert_allclose(
        result["portfolio_history"][dates[1]], expected_after_cost * 1.05
    )
    np.testing.assert_allclose(
        result["portfolio_history"][dates[2]], expected_after_cost * 1.05
    )


def test_reject_leveraged_weights():
    """The strategy is unleveraged; weights above 100% must be rejected."""
    import pytest

    weights = pd.DataFrame(
        0.20,
        index=[pd.Timestamp("2008-01-02")],
        columns=bt.TICKERS,
    )
    with pytest.raises(ValueError, match="sum to at most 1"):
        bt.simulate_portfolio(weights)


def test_frozen_development_final_capital():
    """A regression check for the documented, locally frozen data snapshot."""
    results = bt.simulate_portfolio(bt.execution_weights)
    observed = pd.Series(results["portfolio_history"]).iloc[-1]
    # This published baseline is specific to the user's frozen CSV snapshot.
    np.testing.assert_allclose(observed, 11_589.4846, rtol=0, atol=0.05)
