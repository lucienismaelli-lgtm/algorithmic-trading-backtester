from backtest import Backtest
from data_handler import DataHandler
from strategy import MovingAverageCrossover
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Grid search over MA crossover parameters, visualised as a Sharpe ratio heatmap
    dh = DataHandler("SPY", "2020-01-01", "2024-01-01")
    dh.fetch()
    dh.clean()
    prices = dh.get_prices()

    short_windows = MovingAverageCrossover.param_grid['short_window']
    long_windows = MovingAverageCrossover.param_grid['long_window']
    rows = []
    for short in short_windows:
        for long in long_windows:
            if short < long:
                strategy = MovingAverageCrossover(short, long)
                backtest = Backtest(prices, strategy, initial_cash=10000)
                backtest.run()
                rows.append([short, long, backtest.portfolio.sharpe_ratio(), backtest.portfolio.total_return(), backtest.portfolio.max_drawdown()])

    parameter_grid = pd.DataFrame(rows, columns=['short_window', 'long_window', 'sharpe', 'total_return', 'max_drawdown'])

    pivot = parameter_grid.pivot(index='short_window', columns='long_window', values='sharpe')
    sns.heatmap(pivot, annot=False, fmt='.2f', cmap='RdYlGn')
    plt.title('Sharpe Ratio Heatmap')
    plt.show()