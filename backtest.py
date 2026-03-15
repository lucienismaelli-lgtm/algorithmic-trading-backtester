from portfolio import Portfolio

class Backtest:
    """Orchestrates strategy signal generation and portfolio execution."""

    def __init__(self, prices, strategy, initial_cash, risk_free_rate=0.05, transaction_cost=0.001):
        self.prices = prices
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.risk_free_rate = risk_free_rate
        self.transaction_cost = transaction_cost
    
    def run(self):
        """Generate signals from strategy and run portfolio simulation."""
        signals = self.strategy.generate_signals(self.prices)
        self.portfolio = Portfolio(self.initial_cash, prices=self.prices, signals=signals, risk_free_rate=self.risk_free_rate, transaction_cost=self.transaction_cost)
        self.portfolio.run()
