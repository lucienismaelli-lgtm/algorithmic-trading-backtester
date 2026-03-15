# Algorithmic Trading Backtester

A modular algorithmic trading backtesting framework built in Python from scratch. Designed to test, optimise and validate trading strategies on historical market data, with walk-forward testing to assess out-of-sample performance.

## Project Structure
```
├── data_handler.py       # Downloads and cleans historical price data via yfinance
├── strategy.py           # Abstract base class and concrete strategy implementations
├── portfolio.py          # Simulates trade execution, tracks equity and calculates metrics
├── backtest.py           # Orchestrates strategy signals and portfolio execution
├── results.py            # Generates performance charts and summary statistics
├── optimisation.py       # Grid search over strategy parameters with Sharpe ratio heatmap
├── walk_forward.py       # Walk-forward testing with rolling parameter optimisation
├── multiple_tickers.py   # Compares strategy performance across multiple assets
└── main.py               # Example usage
```

## Strategies

**Moving Average Crossover** - generates a buy signal when the short-term moving average crosses above the long-term moving average, and a sell signal when it crosses below.

**Mean Reversion** - generates a buy signal when price falls more than a threshold number of standard deviations below its rolling mean, and a sell signal when it rises above.

Both strategies use a forward-shifted signal to prevent lookahead bias.

## Performance Metrics

- Annualised Sharpe ratio
- Maximum drawdown
- Total return
- Benchmark comparison against buy-and-hold

## Parameter Optimisation

Grid search across strategy parameters, evaluated by Sharpe ratio and visualised as a heatmap using seaborn.

## Walk-Forward Testing

Splits the price series into n windows. For each window, parameters are optimised on the training portion and evaluated on the unseen test portion. This provides a more robust measure of strategy performance than in-sample optimisation alone.

### Example Output - SPY 2020–2024 (Moving Average Crossover)
```
                          sharpe  total_return  max_drawdown  short_window  long_window
test_period
2020-10-19 to 2021-08-05  1.4381        0.1737       -0.0406            30           60
2021-08-06 to 2022-05-23 -1.5048       -0.1195       -0.1641            30           40
2022-05-24 to 2023-03-13 -1.8632       -0.0981       -0.1090            15          120
2023-03-14 to 2023-12-28 -2.0654       -0.0599       -0.0849            45          120
```

The results show that parameters optimised on one market regime do not generalise well to the next - consistent with the known limitations of trend-following strategies in choppy markets.

### Example Output - GLD 2020–2024 (Mean Reversion)
```
                          sharpe  total_return  max_drawdown  window  threshold
test_period
2020-10-19 to 2021-08-05  0.2292        0.0543       -0.0881    30.0        1.5
2021-08-06 to 2022-05-23 -0.7950       -0.0020       -0.0520    10.0        2.0
2022-05-24 to 2023-03-13  0.1540        0.0490       -0.0576    10.0        2.0
2023-03-14 to 2023-12-28  0.3138        0.0570       -0.0369    10.0        2.0
```

Mean reversion performs more consistently on GLD than SPY, reflecting gold's tendency to oscillate around a mean rather than trend strongly.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from data_handler import DataHandler
from backtest import Backtest
from results import Results
from strategy import MovingAverageCrossover

dh = DataHandler("SPY", "2020-01-01", "2024-01-01")
dh.fetch()
dh.clean()
prices = dh.get_prices()

strategy = MovingAverageCrossover(short_window=20, long_window=50)
backtest = Backtest(prices, strategy, initial_cash=10000)
backtest.run()

results = Results(backtest.portfolio)
results.benchmark_comparison()
results.print_summary()
```

## Dependencies

- pandas
- numpy
- yfinance
- matplotlib
- seaborn
