from backtesting import Backtest


class StrategySimulator:
    def __init__(self, strategy, data, cash=1000, name='default', path=None):
        self.name = name
        self.path = path
        self.eq_final = 0
        self.results = None
        self.bt = Backtest(data=data, strategy=strategy,
                           cash=cash, commission=.002,
                           exclusive_orders=True)

    def backtest(self):
        self.results = self.bt.run()
        self.eq_final = self.results['Equity Final [$]']

    def optimize(self):
        self.backtest()

    def plot(self):
        if self.path is not None:
            filename = self.path + '/' + self.name
            self.bt.plot(filename=filename)
            self.results.to_markdown(buf=filename + "_results.md")
            self.results['_trades'].to_markdown(buf=filename + "_trades.md")
        else:
            self.bt.plot()
            print(self.results)
            print(self.results['_trades'].to_markdown())
