from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from common.indicator import SuperTrend
import pandas as pd
data=pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv',parse_dates=True)
data=data.dropna()
data=data[-20000:]
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator
#from common.indicator import SuperTrend
import numpy as np

hhh = pd.DataFrame()
it = 0


def rs(data):
    global hhh
    global it
    if len(hhh) == 0:
        hhh = ADXIndicator(low=data['Low'], close=data['Close'], high=data['High']).adx()
        # hhh=RSIIndicator(data['Close']).rsi()
    # print(data)
    # print(data)
    it += 1
    print(it)
    return hhh

    # return ADXIndicator(low=data['Low'],close=data['Close'],high=data['High']).adx()


def st(period, multiplier, data):
    p = SuperTrend(data, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close'])
    # trend=p['STX_80_3.6']
    # trend[trend=='down']=0
    # trend[trend=='up']=1
    # trend[trend=='nan']=np.nan
    return p[f'ST_{period}_{multiplier}']


class SmaCross(Strategy):
    period = 25
    multiplier = 9
    period1=35
    multiplier1=9
    h = 65

    def init(self):
        price = self.data.Close
        # self.ma1 = self.I(SMA, price, 50)
        # self.ma2 = self.I(SMA, price, 200)
        self.trend = self.I(st, self.period, self.multiplier, self.data.df)
        self.trend1 = self.I(st, self.period1, self.multiplier1, self.data.df)
        #self.rsi = self.I(rs, self.data.df)
        # self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        # self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)

    def next(self):
        if self.trend >= self.data.Close and self.trend1 <= self.data.Close and not self.position.is_short:
            #self.position.close()
            self.sell()
        if self.trend <= self.data.Close and self.trend1 <= self.data.Close and not self.position.is_short:
            self.position.close()
            #self.buy()
        if self.trend <= self.data.Close and self.trend1 >= self.data.Close and not self.position.is_long:
            #self.position.close()
            self.buy()
        if self.trend >= self.data.Close and self.trend1 >= self.data.Close and not self.position.is_long:
            self.position.close()
            #self.sell()


bt = Backtest(data, SmaCross, commission=0.002, trade_on_close=True, cash=1000000000000, exclusive_orders=True)
stats = bt.run()
bt.plot()
import numpy as np

stats = bt.optimize(period=range(5, 100, 10),
    multiplier=np.arange(2,10,0.5).tolist(),
    period1=range(5, 100, 10),
    multiplier1=np.arange(2,10,0.5).tolist(),
    #h=range(1, 100, 5),
    maximize='Return [%]', return_heatmap=True)

