from data_handler import DataHandler
from backtest import Backtest
import pandas as pd
import numpy as np
import itertools

class WalkForward:

    def __init__(self, ticker, start, end, strategy_class, initial_cash, n_splits=5):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.strategy_class = strategy_class
        self.initial_cash = initial_cash
        self.n_splits = n_splits
        self.param_grid = self.strategy_class.param_grid

    def run(self):
        dh = DataHandler(self.ticker, self.start, self.end)
        dh.fetch()
        dh.clean()
        prices = dh.get_prices()
        chunk_size = len(prices) // self.n_splits
        rows = []
        index = []
        for idx in range(1, self.n_splits):
            train_prices = prices.iloc[: idx * chunk_size]
            test_prices = prices.iloc[idx * chunk_size:(idx + 1) * chunk_size]
            params = self._optimize(train_prices)
            rows.append((params, *self._test(params, test_prices)))
            index.append(f"{test_prices.index[0].date()} to {test_prices.index[-1].date()}")
        results = pd.DataFrame(rows, columns=['params', 'sharpe', 'total_return', 'max_drawdown'])
        results = pd.concat([results.drop('params', axis=1), results['params'].apply(pd.Series)], axis=1)
        results.index = index
        results.index.name = 'test_period'
        return results
    
    def _optimize(self, prices):
        param_grid = self.strategy_class.param_grid
        keys = param_grid.keys()
        values = param_grid.values()
        best_params, best_sharpe = None, None
        for combination in itertools.product(*values):
            params = dict(zip(keys, combination))
            if 'short_window' in params and 'long_window' in params:
                if params['short_window'] > params['long_window']:
                    continue   
            strategy = self.strategy_class(**params)
            signals = strategy.generate_signals(prices)
            num_trades = signals.diff().ne(0).sum()
            if num_trades < 5:
                continue
            backtest = Backtest(prices, strategy, initial_cash=self.initial_cash)
            backtest.run()
            sharpe = backtest.portfolio.sharpe_ratio()
            if (best_sharpe is None or sharpe > best_sharpe):
                best_params = params
                best_sharpe = sharpe
        return best_params

    def _test(self, params, prices):
        strategy = self.strategy_class(**params)
        backtest = Backtest(prices, strategy, initial_cash=self.initial_cash)
        backtest.run()
        return backtest.portfolio.sharpe_ratio(), backtest.portfolio.total_return(), backtest.portfolio.max_drawdown()

if __name__ == "__main__":
    from strategy import MeanReversion
    wf = WalkForward("GLD", "2020-01-01", "2024-01-01", MeanReversion, initial_cash=10000, n_splits=5)
    results = wf.run()
    print("Mean Reversion:")
    print(f"\nWalk-Forward Results: {wf.ticker} ({wf.start} to {wf.end})")
    print(results)