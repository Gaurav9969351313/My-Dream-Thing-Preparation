from backtesting import Strategy
from backtesting.lib import crossover
from talib import EMA

from strategies.StrategySimulator import StrategySimulator


class EmaCross(Strategy):
    n1 = 50
    n2 = 200

    def init(self):
        close = self.data.Close
        self.ema1 = self.I(EMA, close, self.n1)
        self.ema2 = self.I(EMA, close, self.n2)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()


class EmaSimulator(StrategySimulator):
    def __init__(self, data, cash=1000, path=None):
        super().__init__(strategy=EmaCross, data=data, cash=cash, name="EmaCrossover", path=path)

    def optimize(self):
        self.results = self.bt.optimize(n1=range(30, 60, 5), n2=range(180, 210, 5), maximize='Equity Final [$]',
                                constraint=lambda p: p.n1 < p.n2)
        self.eq_final = self.results['Equity Final [$]']