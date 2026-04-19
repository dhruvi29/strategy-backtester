import yfinance as yf
import pandas as pd
import datetime
from data.securities import NIFTY50

UNIVERSE_TICKERS_MAP = {
    'NIFTY50': NIFTY50
}

# ['1m','2m','5m','15m','30m','60m','90m','1h'] -> Not supporting intraday data for now
VALID_INTERVALS = ['1d','5d','1wk','1mo','3mo'] 

class DataLoader:


    def __init__(self,universe : str, start_date : datetime, end_date : datetime, interval : str) -> None:
        self.startDate = start_date
        self.endDate = end_date
        self.interval = interval
        self.universe = universe
        self._validate_params()
        self.ticker_names = self.get_tickers()
        self.tickers = yf.Tickers(','.join(self.ticker_names))
        self.data = self.tickers.download(start = self.startDate, end = self.endDate, interval = self.interval)

    def get_data(self) -> pd.DataFrame:
        return self.data
    
    def get_closing_prices(self) -> pd.DataFrame:
        return self.data['Close']
    
    def _validate_params(self) -> None:
        
        if self.interval not in VALID_INTERVALS:
            raise ValueError(f"Interval {self.interval} not supported")
        if self.startDate >= self.endDate:
            raise ValueError("Start date must be before end date")
        if self.endDate > datetime.date.today():
            raise ValueError("End date must not be greater than today")
        if self.universe not in UNIVERSE_TICKERS_MAP:
            raise ValueError(f"Universe {self.universe} not supported")

    def get_tickers(self) -> list:
        return UNIVERSE_TICKERS_MAP.get(self.universe, None) # Worst case O(n); 