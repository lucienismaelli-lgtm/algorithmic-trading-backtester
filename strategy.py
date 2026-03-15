from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class Strategy(ABC):
    """Abstract base class for trading strategies."""

    def generate_signals(self, prices):
        """Generate forward-filled, lag-adjusted signals from raw strategy output."""
        raw = self._raw_signals(prices)
        signals = pd.Series(raw, index=prices.index).replace(0, np.nan).ffill().fillna(0)
        signals = signals.shift(1).fillna(0)
        return signals
    
    @abstractmethod
    def _raw_signals(self, prices):
        """Return raw signal array of 1 (buy), -1 (sell), 0 (neutral)."""
        pass

class MovingAverageCrossover(Strategy):
    """Buy when short MA crosses above long MA, sell when it crosses below."""

    param_grid = {
        'short_window': range(5, 50, 5),
        'long_window': range(20, 200, 20)
    }

    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window
    
    def _raw_signals(self, prices):
        """Calculate crossover signals from short and long moving averages."""
        short_ma = prices.rolling(self.short_window).mean()
        long_ma = prices.rolling(self.long_window).mean()
        return np.where(short_ma > long_ma, 1, np.where(short_ma < long_ma, -1, 0))
    

class MeanReversion(Strategy):
    """Buy when price is below the mean by threshold standard deviations, sell when above."""
    
    param_grid = {
        'window': range(10, 100, 10),
        'threshold': [0.5, 1.0, 1.5, 2.0]
    }

    def __init__(self, window, threshold):
        self.threshold = threshold
        self.window = window

    def _raw_signals(self, prices):
        """Calculate mean reversion signals using rolling z-score."""
        rolling_mean = prices.rolling(self.window).mean()
        rolling_std = prices.rolling(self.window).std()
        return np.where((prices - rolling_mean) / rolling_std < - self.threshold, 1, np.where((prices - rolling_mean) / rolling_std > self.threshold, -1, 0))
