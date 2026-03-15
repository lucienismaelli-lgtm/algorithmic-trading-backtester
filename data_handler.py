import yfinance as yf

class DataHandler:
    """Handles downloading and cleaning of historical price data via yfinance."""
    
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = None

    def fetch(self):
        """Download OHLCV data for the given ticker and date range."""
        self.data = yf.download(tickers=self.ticker, start=self.start, end=self.end)
        return self.data

    def clean(self):
        """Remove rows with missing values."""
        self.data = self.data.dropna()

    def get_prices(self):
        """Return closing price series."""
        prices = self.data["Close"].squeeze()
        return prices
