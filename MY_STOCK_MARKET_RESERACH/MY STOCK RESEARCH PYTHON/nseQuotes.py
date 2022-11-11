from ast import If
from nsetools import Nse
from pprint import pprint
import pandas as pd
from nsepy import get_history
from datetime import date

pd.set_option('display.max_colwidth', None)

IS_DEBUG_ENABLED = True

INDEX_QUOTES_TO_CONSIDER = [
    {"name": "NIFTY 50" },
    {"name": "NIFTY BANK" },
    {"name": "NIFTY MIDCAP 50" },
    {"name": "NIFTY MIDCAP 100" },
    {"name": "NIFTY IT" },
    {"name": "NIFTY SMLCAP 50" }
]

# hQuotes = get_history(symbol='SBIN', start=date(2022,9,1), end=date(2022,9,18)) # Returns DF
# print(hQuotes.head(3))

nseObj = Nse()

# q = nseObj.get_quote('infy')
# df = pd.DataFrame([q])
# print(df)

def getAdvancesAndDeclines():
    adv_dec = nseObj.get_advances_declines()
    df_adv_dec = df = pd.DataFrame(adv_dec)
    printSection(df_adv_dec)

def getTopLoosersAndGainers():
    top_gainers = nseObj.get_top_gainers()
    df_top_gainers = df = pd.DataFrame(top_gainers)
    printSection(df_top_gainers)

    top_losers = nseObj.get_top_losers()
    df_top_losers = pd.DataFrame(top_losers)
    printSection(df_top_losers)
    return df_top_losers, df_top_gainers 

def getAllIndexQuotes():
    indexQuotes = []
    for i in INDEX_QUOTES_TO_CONSIDER:
        index_quote = nseObj.get_index_quote(i["name"])
        indexQuotes.append(index_quote)
    index_quotes_df = pd.DataFrame(indexQuotes)
    printSection("Index Quotes", index_quotes_df)

def printSection(h3, df):
    if IS_DEBUG_ENABLED:
        print("==============================================================")
        print(h3)
        print(df)
        print("==============================================================") 
    

getAllIndexQuotes()
# getTopLoosersAndGainers()
# getAdvancesAndDeclines()
    
# lot_size = nseObj.get_fno_lot_sizes()
# df_lot_size = pd.DataFrame(lot_size)
# print(df_lot_size)

# index_codes = nseObj.get_index_list()
# index_codes_df = pd.DataFrame(index_codes)
# print(index_codes_df)
