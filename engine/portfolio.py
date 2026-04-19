import pandas as pd
import datetime
class Portfolio:
    def __init__(self, cash: float, security_universe: list) -> None:
        self.cash = cash
        self.tickers = security_universe
        self.N = len(self.tickers)
        self.holdings = pd.DataFrame(columns=self.tickers)
        self.prices = pd.DataFrame(columns=self.tickers)
        self.value = pd.Series()
        self.current_value = 0.0
        self.current_holdings = pd.Series(0, index=self.tickers)

    def execute_trade(self, signal: pd.Series, price: pd.Series, date : datetime.date):
        self.holdings.loc[date] = self.current_holdings + signal
        self.prices.loc[date] = price
        self.value.loc[date] = (self.holdings.loc[date] * price).sum()
        self.current_value = self.value.loc[date]
        self.current_holdings = self.holdings.loc[date]

    def get_current_value(self):
        return self.current_value
    
    def get_curr_positions(self):
        return self.current_holdings
    
    def get_value_history(self):
        return self.value