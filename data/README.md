# Historical inputs

The backtest uses two local, **unchanged** CSV files in this directory:

- `etf_prices.csv`: `Date` index and adjusted closing prices for `SPY`, `EFA`, `EEM`, `AGG`, `GLD`, `DBC`, originally downloaded from `yfinance` with `auto_adjust=True`. The uploaded data span **2006-02-06 to 2026-09-30**.
- `dff_rates.csv`: `observation_date` index and `DFF` annual rates in **decimal** units (`0.04` means 4%), sourced from FRED's DFF series and divided by 100 before saving. The uploaded file runs through **2026-11-02**.

Source references: [yfinance download documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html) and [FRED DFF](https://fred.stlouisfed.org/series/DFF).

**Reproducibility rule:** Keep the original CSV files unchanged. Do not refresh or overwrite them during research or validation; if you later update the data, save a separate dated version and document the change. The CSV files are not redistributed in the shared project package; check the original data providers' licensing before publishing market data.

The simulation uses adjusted prices and a theoretical DFF-based cash return; neither corresponds to guaranteed live execution or a retail cash account.