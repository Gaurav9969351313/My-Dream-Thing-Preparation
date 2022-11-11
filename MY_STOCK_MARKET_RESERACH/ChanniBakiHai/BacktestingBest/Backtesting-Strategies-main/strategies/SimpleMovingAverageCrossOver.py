from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from strategies.StrategySimulator import StrategySimulator


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


class SmaSimulator(StrategySimulator):
    def __init__(self, data, cash=1000, path=None):
        super().__init__(strategy=SmaCross, data=data, cash=cash, name="SmaCrossover", path=path)

    def optimize(self):
        self.results = self.bt.optimize(n1=range(5, 30, 5), n2=range(10, 70, 5), maximize='Equity Final [$]',
                                constraint=lambda p: p.n1 < p.n2)
        self.eq_final = self.results['Equity Final [$]']
