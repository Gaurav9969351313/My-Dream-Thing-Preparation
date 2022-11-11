import pandas as pd
import requests
from bs4 import BeautifulSoup

# link = "https://chartink.com/screener/test-121377"
link = "https://chartink.com/screener/"
url = 'https://chartink.com/screener/process'

payload = {
    # NOTE Intraday bullish - 5 mins 6 in one indicators, price, volume, BB, st, heikin ashi, ichimoko clouds, RSI
    # NOTE Uncomment below line to find all stocks in cash segment 
    'scan_clause': '( {cash} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
    # NOTE Uncomment below line for nifty 100 stocks
    # 'scan_clause': '( {33619} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
        'and [0] 5 minute close >= latest close and [0] 5 minute volume >= [-1] 5 minute sma( volume,15 ) '\
            'and latest volume >= 100000 and [0] 5 minute close >= [0] 5 minute ema( close,20 ) '\
                'and [-1] 5 minute close >= [-1] 5 minute ema( close,20 ) and latest close >= latest lower bollinger band( 20,2 ) '\
                    'and [0] 5 minute close >= [0] 5 minute supertrend( 7,3 ) and [-1] 5 minute close >= [-1] 5 minute supertrend( 7,3 ) '\
                        'and [0] 5 minute ha-close  >= [-1] 5 minute ha-close  and [-1] 5 minute ha-close  >= [-1] 5 minute ha-open  '\
                            'and [0] 5 minute ichimoku conversion line( 9,26,52 ) >= [0] 5 minute ichimoku base line( 9,26,52 ) '\
                                'and [0] 5 minute ichimoku span a( 9,26,52 ) >= [0] 5 minute ichimoku span b( 9,26,52 ) '\
                                    'and [0] 5 minute rsi( 14 ) >= 50 and [0] 5 minute macd line( 26,12,9 ) >= [0] 5 minute macd signal( 26,12,9 ) '\
                                        'and [0] 5 minute macd histogram( 26,12,9 ) >= 0 and [0] 5 minute close >= [-1] 5 minute close '\
                                            'and( [0] 5 minute close - [0] 5 minute open ) >= 0.30 '\
                                                'and [0] 5 minute close >= [0] 5 minute lower bollinger band( 20,2 ) '\
                                                    'and [0] 5 minute rsi( 14 ) >= [-1] 5 minute rsi( 14 ) ) ) '

    # NOTE Intraday bullish
    # 'scan_clause': '( {33619} ( [0] 15 minute volume > 100000 or [0] 15 minute close > latest ema( close,09 ) and [ -1 ] 15 minute close <= 1 day ago  ema( close,09 ) or [0] 15 minute close > latest ema( close,12 ) and [ -1 ] 15 minute close <= 1 day ago  ema( close,12 ) or [0] 15 minute close > latest sma( close,21 ) and [ -1 ] 15 minute close <= 1 day ago  sma( close,21 ) or [0] 15 minute rsi( 14 ) > 60 and [ -1 ] 15 minute rsi( 14 ) <= 60 or [0] 15 minute close > latest ema( close,06 ) and [ -1 ] 15 minute close <= 1 day ago  ema( close,06 ) ) ) '
    # NOTE intraday bullish stocks
    # 'scan_clause': '( {33619} ( [0] 15 minute sma( close,5 ) > latest sma( close,13 ) '\
    #     'and [0] 15 minute sma( close,13 ) > latest sma( close,21 ) '\
    #         'and latest sma( close,21 ) > latest sma( close,50 ) '\
    #             'and latest sma( close,50 ) > latest sma( close,100 ) '\
    #                 'and latest sma( close,100 ) > latest sma( close,200 ) '\
    #                     'and latest macd signal( 26,12,9 ) > latest macd line( 26,12,9 ) '\
    #                         'and latest rsi( 14 ) < 70 and latest upper bollinger band( 20,2 ) > latest close '\
    #                             'and latest close >= latest sma( close,20 ) and latest volume >= latest max( 20 , latest close ) '\
    #                                 'and latest close <= weekly max( 52 , weekly close ) and latest slow stochastic %k( 14,3 ) <= 70 '\
    #                                     'and latest close >= latest sma( close,5 ) ) ) '
    # NOTE 5 min breakout for nifty 100 stock having price between 50 to 2000
    # This must be run in the morning at 9:21 AM and accordingly trades can be taken
    # 'scan_clause': '( {cash} ( [0] 15 minute close > [-1] 15 minute max( 20 , [0] 15 minute close ) '\
    # 'and [0] 15 minute volume > [0] 15 minute sma( volume,20 ) and latest close >= 50 and latest close <= 2000 and latest volume > 100000) ) '
    # 15 min breakout
    # 'scan_clause': '( {cash} ( [0] 5 minute close > [-1] 5 minute max( 20 , [0] 5 minute close ) '\
    # 'and [0] 5 minute volume > [0] 5 minute sma( volume,20 ) and latest close >= 50 and latest close <= 2000 and latest volume > 100000) ) '

    # NOTE Intraday Mean Reversion - https://chartink.com/screener/intraday-mean-reversion-131
    # 'scan_clause': '( {33489} ( latest close > latest sma( close,200 ) and latest rsi( 2 ) > 50 '\
    #     'and latest close > 1 day ago close * 1.03 and latest close > 50 and latest close < 2000 ) ) '
    # NOTE Swapnaja screener - https://chartink.com/screener/swapnaja-sharma-swing-breakout
    # 'scan_clause': '( {cash} ( [0] 1 hour ema( [0] 1 hour close , 50 ) > [0] 1 hour ema( [0] 1 hour close , 200 ) '\
    #     'and [0] 1 hour close > [0] 1 hour ema( [0] 1 hour close , 50 ) and [0] 1 hour rsi( 3 ) > 80 '\
    #         'and [0] 1 hour macd line( 26,12,9 ) > [0] 1 hour macd signal( 26,12,9 ) and [0] 1 hour close > [-1] 1 hour high '\
    #             'and [-1] 1 hour close > [-1] 1 hour open and latest close <= 2000 ) ) '
    # 'scan_clause': '( {33489} ( latest close > 10 ) )'
    # 'scan_clause': '( {33489} ( latest supertrend( 10,2 ) < latest close and 1 day ago  supertrend( 10,2 ) >= 1 day ago  close ) ) '
    # 'scan_clause': '( {33489} ( latest close > latest ema( close,07 ) and latest rsi( 6 ) > 75 and latest close > 120 '\
    #     'and latest close < 9000 and latest volume > 100000 ) and latest close > latest vwap)'
    # 'scan_clause': '( {33489} ( ( {33489} ( [0] 15 minute ema( close,15 ) > [0] 15 minute ema( high,50 ) '\
    #     'and [ -1 ] 15 minute ema( close,15 )<= [ -1 ] 15 minute ema( high,50 ) and [0] 15 minute close >= [0] 15 minute vwap '\
    #         'and [0] 15 minute volume >= [0] 15 minute sma( volume,15 ) ) ) or( {33489} ( [0] 15 minute ema( close,15 ) < [0] 15 minute ema( low,50 ) '\
    #             'and [ -1 ] 15 minute ema( close,15 )>= [ -1 ] 15 minute ema( low,50 ) and [0] 15 minute close <= [0] 15 minute vwap '\
    #                 'and [0] 15 minute volume >= [0] 15 minute ema( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( close,15 ) > [-1] 15 minute ema( high,50 ) '\
    #                     'and [ -2 ] 15 minute ema( close,15 )<= [ -2 ] 15 minute ema( high,50 ) and [-1] 15 minute close >= [-1] 15 minute vwap '\
    #                         'and [-1] 15 minute volume >= [-1] 15 minute sma( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( low,50 ) < [-1] 15 minute ema( close,15 ) '\
    #                             'and [ -2 ] 15 minute ema( low,50 )>= [ -2 ] 15 minute ema( close,15 ) '\
    #                                 'and [-1] 15 minute close <= [-1] 15 minute vwap and [-1] 15 minute volume >= [-1] 15 minute ema( volume,15 ) ) ) ) )'
}


def buy_stock(symbol, per_chg, qty):
    print(
        f'buying stock :: "{symbol}" :: with percent change :: "{per_chg}" and quantity :: "{qty}"')


def sell_stock(symbol, per_chg, qty):
    print(
        f'selling stock :: "{symbol}" :: with percent change :: "{per_chg}" and quantity :: "{qty}"')

def only_buy(item):
    qty = 10 if item['close'] > 1000 else 25
    print('buying {} quantity of {} shares whose close price is {}'.format(qty, item['nsecode'], item['close']))

with requests.Session() as s:
    r = s.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.select_one("[name='csrf-token']")['content']
    s.headers['x-csrf-token'] = csrf
    r = s.post(url, data=payload)
    # print(r.text)
    # df = pd.DataFrame(columns=['sr', 'nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume'], index=['sr'])
    # print(df.columns)

    df = pd.DataFrame()
    df_sell = pd.DataFrame()
    df_buy = pd.DataFrame()
    for item in r.json()['data']:
        print('======================================')
        # print(item['name'],item['nsecode'],item['per_chg'],item['close'],item['volume'])
        only_buy(item)
        df = df.append(item, ignore_index=True)
    #     pc = float(item['per_chg'])
    #     if pc < 1.5 and pc > 0.5:
    #         df_buy = df_buy.append(item, ignore_index=True)
    #     if pc < -0.5 and pc > -1.5:
    #         df_sell = df_sell.append(item, ignore_index=True)
    # # df_buy.index = df_buy['sr']
    # df_buy.drop('sr', axis=1, inplace=True)
    # print(df_buy)
    # # df_buy.to_csv('chartink_5min_breakout_buy.csv')
    # print('======================================')
    # print('======================================')
    # for symbol, pc in zip(df_buy['nsecode'].values, df_buy['per_chg'].values):
    #     buy_stock(symbol, pc, 10)

    # # df_sell.index = df_sell['sr']
    # df_sell.drop('sr', axis=1, inplace=True)
    # print(df_sell)
    # # df_sell.to_csv('chartink_5min_breakout_sell.csv')
    # print('======================================')
    # print('======================================')
    # for symbol, pc in zip(df_sell['nsecode'].values, df_sell['per_chg'].values):
    #     sell_stock(symbol, pc, 10)

    print('======================================')

    df.index = df['sr']
    df.drop('sr', axis=1, inplace=True)
    print('======================================')
    print('verify with below table')
    print('======================================')

    print(df)
    print('======================================')
    print('======================================')
    # df.to_csv('chartink_5min_breakout.csv')


