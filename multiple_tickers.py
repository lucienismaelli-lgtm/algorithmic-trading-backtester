from data_handler import DataHandler
from backtest import Backtest
from strategy import MovingAverageCrossover
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Compare MA crossover equity curves across multiple tickers
    start = "2020-01-01"
    end = "2024-01-01"
    tickers = ["AAPL", "QQQ", "GLD", "SPY"]

    for ticker in tickers:
        dh = DataHandler(ticker, start, end)
        dh.fetch()
        dh.clean()
        prices = dh.get_prices()
        strategy = MovingAverageCrossover(short_window=35, long_window=180)
        backtest = Backtest(prices, strategy, initial_cash=10000)
        backtest.run()
        backtest.portfolio.equity.plot.line(label=ticker)

    plt.title('Multiple Tickers - Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.show()
