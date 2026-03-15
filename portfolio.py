import pandas as pd
import numpy as np

class Portfolio:
    """Simulates portfolio execution from signals, tracking cash, positions and equity."""

    def __init__(self, initial_cash, prices, signals, risk_free_rate=0.05, transaction_cost=0.001):
        self.initial_cash = initial_cash
        self.prices = prices
        self.signals = signals
        self.risk_free_rate = risk_free_rate
        self.transaction_cost = transaction_cost
        self.cash = pd.Series(0.0, index=prices.index)
        self.position = pd.Series(0.0, index=prices.index)
        self.equity = pd.Series(0.0, index=prices.index)

    def run(self):
        """Execute trades based on signals, applying transaction costs."""
        self.cash.iloc[0] = self.initial_cash
        self.equity.iloc[0] = self.initial_cash
        for idx in range(1, self.prices.size):
            self.cash.iloc[idx] = self.cash.iloc[idx - 1]
            self.position.iloc[idx] = self.position.iloc[idx - 1]
            if self.signals.iloc[idx] == 1 and self.position.iloc[idx] == 0:
                cost = self.cash.iloc[idx] * self.transaction_cost
                self.position.iloc[idx] = (self.cash.iloc[idx] - cost) / self.prices.iloc[idx]
                self.cash.iloc[idx] = 0
            if self.signals.iloc[idx] == -1 and self.cash.iloc[idx] == 0:
                self.cash.iloc[idx] = self.position.iloc[idx] * self.prices.iloc[idx]
                cost = self.cash.iloc[idx] * self.transaction_cost
                self.cash.iloc[idx] -= cost
                self.position.iloc[idx] = 0
            self.equity.iloc[idx] = self.cash.iloc[idx] + self.position.iloc[idx] * self.prices.iloc[idx]
            
    def sharpe_ratio(self):
        """Return annualised Sharpe ratio of the portfolio."""
        daily_returns = self.equity.pct_change().dropna()
        if daily_returns.std() == 0:
            return 0.0
        return round(float((daily_returns.mean() - self.risk_free_rate/252) / daily_returns.std() * np.sqrt(252)), 4)

    def max_drawdown(self):
        """Return maximum peak-to-trough drawdown as a fraction."""
        rolling_max = self.equity.cummax()
        return round(float(min((self.equity-rolling_max) / rolling_max)), 4)

    def total_return(self):
        """Return total return as a fraction of initial cash."""
        return round(float((self.equity.iloc[-1] - self.equity.iloc[0]) / self.equity.iloc[0]), 4)
    