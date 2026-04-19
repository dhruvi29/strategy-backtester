import pandas as pd
import math

class EqualWeightedStrategy:
    def __init__(self):
        pass

    def generate_new_qty(self, portfolio_value: float, curr_prices):

        N = len(curr_prices.keys())
        return ((portfolio_value / N) / curr_prices).apply(math.floor)
    
    def generate_signals(self, portfolio_value: float, curr_prices: pd.Series, previous_qty: pd.Series):
        new_qty = self.generate_new_qty(portfolio_value, curr_prices)
        return new_qty - previous_qty