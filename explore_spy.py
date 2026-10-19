import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

spy = yf.Ticker("SPY")
data = spy.history(
    start="2020-01-01",     # Year-month-day
    end="2021-01-01",
    interval="1d",          # Diario
    auto_adjust=True        # Tener en cuenta dividendos y stock splits
)

print(data.head())              # Devuelve n filas del DataFrame (5 por defecto)
print(data.shape)               # Devuelve las dimensiones de la tabla
print(data.columns)             # Devuelve los 'títulos' de las columnas
print(data.isna().sum())        # Cuenta cuantos NaN hay por columna

close_prices = data["Close"]    # Es una Series con la columna "Close"

print(close_prices.head())       
print(type(close_prices))       # Me dice de que tipo es la variable 

first_price = close_prices.iloc[0]              # Me quedo con la fila n + 1 de mi Series
second_price = close_prices.iloc[1]

daily_return = (second_price - first_price) / first_price

print(daily_return)

daily_returns = close_prices.pct_change()       # Me da una Series con las rentabilidades diarias simples

print(daily_returns.head())

clean_returns = daily_returns.dropna()          # Elimina las filas con NaN

print(clean_returns.shape)
print(clean_returns.head())

mean_daily_return = clean_returns.mean()        # Calcula la media aritmética
daily_volatility = clean_returns.std()          # Calcula la desviación típica muestral

print(mean_daily_return)
print(daily_volatility)

annualized_mean_return = 252 * mean_daily_return
annualized_volatility = np.sqrt(252) * daily_volatility

print(annualized_mean_return)
print(annualized_volatility)

initial_price = close_prices.iloc[0]
final_price = close_prices.iloc[-1]             # Última fila

total_return_1 = final_price / initial_price - 1

print(total_return_1)

total_return_2 = (1 + clean_returns).cumprod().iloc[-1] - 1     # [2,3,4] -> [2,6,24]

print(total_return_2)

print(abs(total_return_1 - total_return_2))                     # Valor absoluto

close_prices.plot()                                             # Eje x: fechas / Eje y: precios de cierre
plt.show()                                                      # Me muestra el gráfico

clean_returns.plot()
plt.axhline(y=0)                                                # Añado la recta horizontal y=0
plt.axhline(y=mean_daily_return)
plt.show()

rolling_volatility = clean_returns.rolling(window=21).std()     # Ventana de volatilidad móvil (uso las 21 rentabilidades previas)
print(rolling_volatility.count())                               # Deveulve el nº de filas sin NaN


rolling_volatility.plot()
plt.show()