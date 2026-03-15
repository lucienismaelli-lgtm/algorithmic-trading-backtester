import matplotlib.pyplot as plt

class Results:
    """Generates performance charts and summary statistics for a completed backtest."""
    
    def __init__(self, portfolio):
        self.portfolio = portfolio
    
    def equity_curve(self):
        """Plot portfolio equity curve over time."""
        self.portfolio.equity.plot.line(title='Equity Curve')
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.show()

    def drawdown_curve(self):
        """Plot portfolio drawdown over time."""
        rolling_max = self.portfolio.equity.cummax()
        drawdown = (self.portfolio.equity - rolling_max) / rolling_max
        drawdown.plot.line(title='Drawdown')
        plt.xlabel('Date')
        plt.ylabel('Drawdown')
        plt.show()

    def print_summary(self):
        """Print total return, Sharpe ratio and max drawdown."""
        print("Total Return: " + str(self.portfolio.total_return()))
        print("Sharpe Ratio: " + str(self.portfolio.sharpe_ratio()))
        print("Max Drawdown: " + str(self.portfolio.max_drawdown()))
    
    def benchmark_comparison(self):
        """Plot strategy equity curve against buy-and-hold benchmark."""
        buy_and_hold = self.portfolio.initial_cash * (self.portfolio.prices / self.portfolio.prices.iloc[0])
        buy_and_hold.plot.line(label='Buy & Hold')
        self.portfolio.equity.plot.line(label='Equity Curve')
        plt.title('Benchmark Comparison')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.show()
