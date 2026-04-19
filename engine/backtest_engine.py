import matplotlib.pyplot as plt
import pandas as pd
import datetime

from strategies.equal_weighted import EqualWeightedStrategy
from data.data_loader import DataLoader
from engine.portfolio import Portfolio

class Engine:
    def __init__(self,universe = 'NIFTY50', initial_capital = 100000000,  strategy = None,  start_date : datetime = datetime.date(2025,1,1), end_date : datetime = datetime.date.today(), interval : str = '1mo'):
        self.strategy = EqualWeightedStrategy()
        self.initial_capital = initial_capital
        self.data_loader = DataLoader(universe, start_date, end_date, interval)
        self.closing_prices = self.data_loader.get_closing_prices()
        self.portfolio = Portfolio(initial_capital, self.data_loader.get_tickers())

        self.open_positions = pd.Series(0, index=self.data_loader.get_tickers())
        self.begin_capital = initial_capital
        self.begin_price = self.closing_prices.iloc[0]

    def run_backtest(self):
        for curr_date, curr_price in self.closing_prices.iterrows():

            signals = self.strategy.generate_signals(self.begin_capital, self.begin_price, self.open_positions)
            self.portfolio.execute_trade(signals, curr_price, curr_date)
            self.open_positions = self.portfolio.get_curr_positions()
            self.begin_capital = self.portfolio.get_current_value()
            self.begin_price = curr_price

    def get_performance(self):
        return plt.plot(self.portfolio.get_value_history())