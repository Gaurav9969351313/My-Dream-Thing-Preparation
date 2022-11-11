from backtesting import Strategy
from backtesting.lib import crossover
from talib import STOCH

from strategies.StrategySimulator import StrategySimulator


class StocOscCross(Strategy):
    fast_k = 14
    slow_k = 7
    slow_d = 3


    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        self.so = self.I(STOCH, high, low, close, self.fast_k, self.slow_k, 0, self.slow_d, 0)

    def next(self):
        if crossover(self.so[0], self.so[1]) and self.so[0] < 20:
            self.buy()
        elif crossover(self.so[1], self.so[0]) and self.so[0] > 80:
            self.sell()


class StochSimulator(StrategySimulator):
    def __init__(self, data, cash=1000, path=None):
        super().__init__(strategy=StocOscCross, data=data, cash=cash, name="StochOscCrossover", path=path)

    def optimize(self):
        self.results = self.bt.optimize(fast_k=range(5, 14, 1), slow_k=range(3, 7, 1), maximize='Equity Final [$]',
                                constraint=lambda p: p.slow_k < p.fast_k)
        self.eq_final = self.results['Equity Final [$]']
