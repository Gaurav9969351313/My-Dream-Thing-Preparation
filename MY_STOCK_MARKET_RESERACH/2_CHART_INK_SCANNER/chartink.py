import logging
import os
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep

import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
# NOTE while creating date objects you can use zone info which is very helpful when you are running scripts on outside India location
zone = pytz.timezone('Asia/Kolkata')


def get_stocks():

    with requests.Session() as s:
        scanner_url = 'https://chartink.com/screener/copy-vishal-mehta-mean-reversion-56'
        r = s.get(scanner_url)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf

        process_url = 'https://chartink.com/screener/process'
        payload = {
            # NOTE Vishal Mehta Mean Reversion Selling - Place Limit Order at 1% of Latest Close Price 3% SL and 6% Target Exit all positions at 3PM
            'scan_clause': '( {33489} ( latest close > latest sma( close, 200 ) and latest rsi( 2 ) > 50 and '\
            'latest close > 1 day ago close * 1.03 and latest close > 200 and latest close < 5000 and latest close > ( 4 days ago close * 1.0 ) ) ) '
        }

        r = s.post(process_url, data=payload)
        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
        # NOTE Sorting done by ascending price so that stock with less price can be purchased before
        # Costly stocks may be rejected if there is no capital
        df.sort_values(by=['close'], inplace=True)
        df.drop('sr', axis=1, inplace=True)
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)

        print(f'number of stocks :: {len(df)}')
        if len(df) > 10:
            print('returning only first 10 stocks')
            df = df.head(10)
        return df


if __name__ == "__main__":
    global kite

    begin_time = dt.now(tz=zone)
    print(begin_time)

    stocks = get_stocks()
    print(stocks)
