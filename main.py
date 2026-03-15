from data_handler import DataHandler
from backtest import Backtest
from results import Results
from strategy import MovingAverageCrossover, MeanReversion

if __name__ == "__main__":
    strategy = MovingAverageCrossover(short_window=20, long_window=50)
    dh = DataHandler("SPY", "2020-01-01", "2024-01-01")
    dh.fetch()
    dh.clean()
    prices = dh.get_prices()
    backtest = Backtest(prices, strategy, initial_cash=10000)
    backtest.run()
    results = Results(backtest.portfolio)

    print("Moving Average Crossover")
    results.equity_curve()
    results.benchmark_comparison()
    results.drawdown_curve()
    results.print_summary()

    strategy = MeanReversion(window=20, threshold=1.5)
    backtest = Backtest(prices, strategy, initial_cash=10000)
    backtest.run()

    results = Results(backtest.portfolio)

    print("Mean Reversion")
    results.equity_curve()
    results.benchmark_comparison()
    results.drawdown_curve()
    results.print_summary()
