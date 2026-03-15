from backtest import Backtest
from strategy import MovingAverageCrossover
import pandas as pd
import matplotlib.pyplot as plt

start = "2020-01-01"
end = "2024-01-01"
tickers = ["AAPL", "QQQ", "GLD", "SPY"]
for ticker in tickers:
    strategy = MovingAverageCrossover(short_window=35, long_window=180)
    backtest = Backtest(ticker, start, end, strategy, initial_cash=10000)
    backtest.run()
    backtest.portfolio.equity.plot.line(label=ticker)
plt.title('Multiple Tickers - Equity Curve')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.show()
