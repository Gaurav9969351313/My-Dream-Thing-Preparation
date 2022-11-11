import pandas as pd
import requests
from bs4 import BeautifulSoup

# link = "https://chartink.com/screener/test-121377"
link = "https://chartink.com/screener/"
url = 'https://chartink.com/screener/process'

payload = {
    # NOTE Swapnaja screener - https://chartink.com/screener/swapnaja-sharma-swing-breakout
    'scan_clause': '( {cash} ( [0] 1 hour ema( [0] 1 hour close , 50 ) > [0] 1 hour ema( [0] 1 hour close , 200 ) '\
        'and [0] 1 hour close > [0] 1 hour ema( [0] 1 hour close , 50 ) and [0] 1 hour rsi( 3 ) > 80 '\
            'and [0] 1 hour macd line( 26,12,9 ) > [0] 1 hour macd signal( 26,12,9 ) '\
                'and [0] 1 hour close > [-1] 1 hour high and [-1] 1 hour close > [-1] 1 hour open and latest close <= 2100 and latest volume > 100000) ) '
    # 'scan_clause': '( {33489} ( latest close > 10 ) )'
    # 'scan_clause': '( {33489} ( latest supertrend( 10,2 ) < latest close and 1 day ago  supertrend( 10,2 ) >= 1 day ago  close ) ) '
    # 'scan_clause': '( {33489} ( latest close > latest ema( close,07 ) and latest rsi( 6 ) > 75 and latest close > 120 and latest close < 9000 and latest volume > 100000 ) and latest close > latest vwap)'
    # 'scan_clause': '( {33489} ( ( {33489} ( [0] 15 minute ema( close,15 ) > [0] 15 minute ema( high,50 ) and [ -1 ] 15 minute ema( close,15 )<= [ -1 ] 15 minute ema( high,50 ) and [0] 15 minute close >= [0] 15 minute vwap and [0] 15 minute volume >= [0] 15 minute sma( volume,15 ) ) ) or( {33489} ( [0] 15 minute ema( close,15 ) < [0] 15 minute ema( low,50 ) and [ -1 ] 15 minute ema( close,15 )>= [ -1 ] 15 minute ema( low,50 ) and [0] 15 minute close <= [0] 15 minute vwap and [0] 15 minute volume >= [0] 15 minute ema( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( close,15 ) > [-1] 15 minute ema( high,50 ) and [ -2 ] 15 minute ema( close,15 )<= [ -2 ] 15 minute ema( high,50 ) and [-1] 15 minute close >= [-1] 15 minute vwap and [-1] 15 minute volume >= [-1] 15 minute sma( volume,15 ) ) ) or( {33489} ( [-1] 15 minute ema( low,50 ) < [-1] 15 minute ema( close,15 ) and [ -2 ] 15 minute ema( low,50 )>= [ -2 ] 15 minute ema( close,15 ) and [-1] 15 minute close <= [-1] 15 minute vwap and [-1] 15 minute volume >= [-1] 15 minute ema( volume,15 ) ) ) ) )'
}
with requests.Session() as s:
    r = s.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.select_one("[name='csrf-token']")['content']
    s.headers['x-csrf-token'] = csrf
    r = s.post(url, data=payload)
    df = pd.DataFrame(columns=['sr', 'nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume'], index=None)
    print(df.columns)
    
    # df = pd.DataFrame()
    for item in r.json()['data']:
        # print(item['name'],item['nsecode'],item['per_chg'],item['close'],item['volume'])
        # print(item)
        df = df.append(item, ignore_index=True)
    # df.index = df['sr']
    # df.drop('sr', axis=1, inplace=True)
    print(df)
    # df.to_csv('chartink.csv')
