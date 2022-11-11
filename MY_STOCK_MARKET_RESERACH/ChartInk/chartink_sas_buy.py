import json
import logging
import sys
import time
from collections import namedtuple
# Same script can be used for alice blue but might have to change some API calls
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
from enum import Enum
from time import sleep

import pandas as pd
import requests
from alphatrade import AlphaTrade, OrderType, ProductType, TransactionType
from bs4 import BeautifulSoup

import config

# NOTE This includes every candle strategy and inside bar strategy


# NOTE Contents of config file must be as below
# login_id = "RR24980"
# twofa = "rr"

# password = "53crEt@1"

# try:
#     access_token = open('access_token.txt', 'r').read().rstrip()
# except Exception as e:
#     print('Exception occurred :: {}'.format(e))
#     access_token = None


start = dt.now()
print(start)

# Optional for getting debug messages.
logfile = dt.now().strftime("%d-%m-%Y_%H%M%S")+"ec.log"
print(logfile)
logging.basicConfig(level=logging.INFO, filename=logfile, filemode='w')


def log(msg, *args):
    logging.info(msg, *args)
    print(msg, *args)


sas = None

sas = AlphaTrade(login_id=config.login_id, password=config.password,
                 twofa=config.twofa, access_token=config.access_token, master_contracts_to_download=['NSE'])

scrip = None



# link = "https://chartink.com/screener/test-121377"
link = "https://chartink.com/screener/"
url = 'https://chartink.com/screener/process'

payload = {
    # NOTE Intraday bullish - 5 mins 6 in one indicators, price, volume, BB, st, heikin ashi, ichimoko clouds, RSI
    # NOTE Uncomment below line to find all stocks in cash segment 
    'scan_clause': '( {cash} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
    # NOTE Uncomment below line for nifty 100 stocks
    # 'scan_clause': '( {33619} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
    # NOTE Uncomment below for nifty 200 stocks
    # 'scan_clause': '( {46553} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
    # NOTE Uncomment below for nifty 500 stocks
    # 'scan_clause': '( {57960} ( ( [0] 5 minute high - [0] 5 minute low ) >= 0.30 and [-1] 5 minute close >= [-1] 5 minute open '\
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
}


def only_buy(item):
    global sas, scrip
    qty = 10 if item['close'] > 1000 else 25
    scrip = sas.get_instrument_by_symbol(exchange='NSE', symbol=item['nsecode'])
    # print('buying {} quantity of {} shares whose close price is {}'.format(qty, scrip, item['close']))
    return {
        "instrument": sas.get_instrument_by_symbol('NSE', item['nsecode']),
        "order_type": OrderType.Market,
        "quantity": qty,
        "price": 0.0,
        "transaction_type": TransactionType.Buy,
        "product_type": ProductType.Intraday,
    }
    
    

with requests.Session() as s:
    r = s.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.select_one("[name='csrf-token']")['content']
    s.headers['x-csrf-token'] = csrf
    r = s.post(url, data=payload)

    orders = []

    df = pd.DataFrame()
    df_sell = pd.DataFrame()
    df_buy = pd.DataFrame()
    for item in r.json()['data']:
        print('======================================')
        # print(item['name'],item['nsecode'],item['per_chg'],item['close'],item['volume'])
        orders.append(only_buy(item))
        df = df.append(item, ignore_index=True)

        print('======================================')

    df.index = df['sr']
    df.drop('sr', axis=1, inplace=True)
    print('======================================')
    print('verify with below table')
    print('======================================')

    print(df)
    print('======================================')
    print('======================================')
    # print(orders)
    result = sas.place_basket_order(orders)
    print(result)
    book = sas.get_order_history()
    print(book)
    log_date = dt.now().strftime('%d-%m-%Y_%H%M')
    # NOTE Check below if completed_orders is present or not.
    order_history = sas.get_order_history()['data']
    try:
        df = pd.DataFrame.from_dict(order_history['completed_orders'])
        df.to_csv('{}_order_history.csv'.format(log_date))
    except Exception as e:
        log(f'exception occurred {e}')

