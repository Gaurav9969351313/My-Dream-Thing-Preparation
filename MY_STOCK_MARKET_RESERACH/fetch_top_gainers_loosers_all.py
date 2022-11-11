import json
import requests
import typing
from requests.models import PreparedRequest
from pprint import pprint

HEADERS = {'user-agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36',
           'accept-encoding':
           'gzip, deflate, br'
           }

ROUTES = {
    "base": "https://www.nseindia.com",
    "api": "/api",
    "live-analysis": "/live-analysis-variations",
    "snapshot-derivatives-equity": "/snapshot-derivatives-equity",
    "currency-derivatives": "/currency-derivatives",
    "commodity-futures": "/commodity-futures",
    "equity-derivatives": "/liveEquity-derivatives",
    "quote-derivative": "/quote-derivative"
}


def get_url(route: str, params: typing.Dict[str, str]={}):
    raw_url = PreparedRequest()
    if params:
        raw_url.prepare_url(f"{ROUTES['base']}{ROUTES['api']}{ROUTES[route]}", params)
        return raw_url.url
    else:
        raw_url.prepare_url(f"{ROUTES['base']}{ROUTES['api']}{ROUTES[route]}", params)
        return raw_url.url


def get_equity_quote_derivative(_symbol: str):
    return session.get(
        get_url('quote-derivative', {'symbol': _symbol.upper()}), headers=HEADERS).json()

if __name__ == "__main__":
    session = requests.session()
    response = session.get("https://www.nseindia.com/", headers=HEADERS)
    top_twenty_gainers = session.get(
        get_url('live-analysis', {'index': 'gainers'}), headers=HEADERS).json()
    top_twenty_loosers = session.get(
        get_url('live-analysis', {'index': 'loosers'}), headers=HEADERS).json()
    most_active_fno = session.get(
        get_url('snapshot-derivatives-equity', {'index': 'contracts', 'limit': 20}), headers=HEADERS).json()
    most_active_cfo = session.get(
        get_url('currency-derivatives', {'index': 'most_act_cont'}), headers=HEADERS).json()
    most_active_cf = session.get(
        get_url('commodity-futures'), headers=HEADERS).json()
#################################### New Addition ########################
    top_twenty_stock_futures = session.get(
        get_url('equity-derivatives', {'index': 'stock_fut'}), headers=HEADERS).json()
    top_twenty_stock_options = session.get(
        get_url('equity-derivatives', {'index': 'stock_opt'}), headers=HEADERS).json()
    reliance_derivative_data = get_equity_quote_derivative("reliance")
##########################################################################

    print("TOP_TWENTY_GAINERS ➨")
    pprint(top_twenty_gainers)
    print("TOP_TWENTY_LOOSERS ➨")
    pprint(top_twenty_loosers)
    print("TOP_TWENTY_MOST_ACTIVE_FNO_CONTRACTS ➨")
    pprint(most_active_fno)
    print("TOP_TWENTY_MOST_ACTIVE_CFO_CONTRACTS ➨")
    pprint(most_active_cfo)
    print("TOP_TWENTY_MOST_ACTIVE_COMMODITY_CONTRACTS ➨")
    pprint(most_active_cf)
#################################### New Addition ########################
    print("TOP_TWENTY_MOST_ACTIVE_STOCK_FUTURES ➨")
    pprint(top_twenty_stock_futures)
    print("TOP_TWENTY_MOST_ACTIVE_STOCK_OPTIONS ➨")
    pprint(top_twenty_stock_options)
    print("RELIANCE_STOCK_OPTIONS_FUTURES ➨")
    pprint(reliance_derivative_data)
##########################################################################
