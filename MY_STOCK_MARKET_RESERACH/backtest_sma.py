import yfinance as yf
import talib
import pandas as pd
import copy
import numpy as np
from pandas import Series
# from gym import spaces
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, EMA

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


def symbols_backtesting(symbol):
    all_trades = []
    # for symbol in symbol_list:
    df = yf.Ticker(f"{symbol}.NS").history(period="2y", interval="1d")
    df["MA_10"] = talib.MA(df["Close"], timeperiod=10)
    df["MA_20"] = talib.MA(df["Close"], timeperiod=20)
    df["RSI_14"] = talib.RSI(df["Close"], timeperiod=14)
    df["ATR_14"] = talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)
    df["Upper_Band"], df["Middle_Band"], df["Lower_Band"] = talib.BBANDS(df["Close"], timeperiod=20, nbdevup=2,nbdevdn=2)
    return df

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 35
    rsi_window  = 14 

    def init (self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)
        
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()    
        
class SmaCross(Strategy):
    def init(self):
        print("Init called")
        # price = self.data.Close
        # self.MA_10 = self.I(SMA, price, 10)
        # self.MA_20 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.data.MA_10, self.data.MA_20):
            self.buy()
        elif crossover(self.data.MA_20, self.data.MA_10):
            self.sell()


def EMA(arr, n, k):
    weights=np.power(1-k, list(reversed(range(n))))
    weights/=np.sum(weights)
    return Series(arr).rolling(n).apply(lambda x: np.sum(weights*x), raw=False)
    
class EmaCross(Strategy):
    n1, n1_base = None, 13  # short EMA
    n2, n2_base = None, 48  # long EMA
    k = 0.1
    action_space = spaces.Box(
        np.array([1, 1], dtype=np.float32),
        np.array([24 * 18, 24 * 18], dtype=np.float32),
        dtype=np.float32
    )

    def init(self):
        self.n1 = int(round(self.n1))
        self.n2 = int(round(self.n2))
        self.ema1 = self.I(EMA, self.data.Close, self.n1, self.k)
        self.ema2 = self.I(EMA, self.data.Close, self.n2, self.k)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()

# bt = Backtest(symbols_backtesting("UPL"), SmaCross,cash=100000, commission=.002, exclusive_orders=True)
bt = Backtest(symbols_backtesting("UPL"), RsiOscillator, cash=100000, commission=.002, exclusive_orders=True)
stats = bt.run()
print(stats)
# bt.plot()