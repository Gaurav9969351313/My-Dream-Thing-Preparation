from nsepython import *   
from  datetime import datetime, date
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(
    page_title = 'Pattern Watcher',
    layout = 'wide'
)


# key = "NIFTY"
# key = "BANKNIFTY"
# key = "FO"

def nse_preopen(key="NIFTY"):
    returnTo = []
    payload = nsefetch("https://www.nseindia.com/api/market-data-pre-open?key="+key+"")   
    dataList = payload['data']
    for d in dataList:
        obj = {}
        obj['lastUpdateTime'] = d['detail']['preOpenMarket']['lastUpdateTime']
        obj['symbol'] = d['metadata']['symbol']
        obj['lastPrice'] = d['metadata']['lastPrice']
        obj['change'] = d['metadata']['change']
        obj['pChange'] = d['metadata']['pChange']
        obj['previousClose'] = d['metadata']['previousClose']
        # obj['yearHigh'] = d['metadata']['yearHigh']
        # obj['yearLow'] = d['metadata']['yearLow']
        returnTo.append(obj)
    return returnTo

def get_option_chain(symbol):
    try:
        symbol = symbol.upper()
        option_chain_json = nse_optionchain_scrapper(symbol)
        data = option_chain_json['filtered']['data']
        return data
    except:
        pass

def get_atm_strike(option_chain_data):
    try:
        ltp = option_chain_data[0]['PE']['underlyingValue']
        strike_price_list = [x['strikePrice'] for x in option_chain_data]
        atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
        return atm_strike
    except:
        return 0

def get_pe_ce_price(atm_strike, option_chain_data):
    for dictt in option_chain_data:
        if dictt['strikePrice'] == atm_strike:
            pe_price = dictt['PE']['askPrice']
            ce_price = dictt['CE']['askPrice']
            return pe_price,ce_price
        
def getTokenDf():
    token_df = pd.read_json("./OpenAPIScripMaster.json")
    token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
    token_df = token_df.astype({'strike': float})
    return token_df

def getTokenInfo (symbol, exch_seg ='NSE',instrumenttype='OPTIDX',strike_price = '',pe_ce = 'CE',expiry_day = None):
    df = getTokenDf()
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['expiry']==expiry_day) &  (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

def getFinalData(pre_dict):
    f_preopen = []
    expiry_day = date(2022,11,24)
    for i in pre_dict.keys():
        actual = pre_dict.get(i)
        try: 
            option_chain_data = get_option_chain(actual['symbol'])
            actual['atm_strike'] = get_atm_strike(option_chain_data)
            if actual['atm_strike'] != 0:
                
                ce_ltp, pe_ltp = get_pe_ce_price(actual['atm_strike'], option_chain_data)
                actual['CE_LTP'] = ce_ltp
                actual['CE_SL'] = ce_ltp * 1.10
                actual['PE_LTP'] = pe_ltp
                actual['PE_SL'] = pe_ltp * 1.10
                tokenInfo = getTokenInfo(actual['symbol'], 'NFO', 'OPTSTK', actual['atm_strike'], 'CE', expiry_day).iloc[0]
                actual['lotsize'] = int(tokenInfo['lotsize'])
                actual['token'] = int(tokenInfo['token'])
                actual['full_symbol'] = tokenInfo['symbol']
                actual['funds_req_ce_buy'] = ce_ltp * actual['lotsize']
            f_preopen.append(actual)
        except:
            pass
    return f_preopen

def printAnalysis(df):
    pre_buy_opp_dict = df.to_dict('index')
    f_propen_buy = getFinalData(pre_buy_opp_dict)
    fdf_buy_oppurtunity =  pd.DataFrame.from_dict(f_propen_buy)
    return fdf_buy_oppurtunity

def app():
    start = time.time() 
    preeopen_df = pd.DataFrame(nse_preopen("NIFTY"))
    f_preeopen_buy_opp_df = preeopen_df.head(10)
    
    st.markdown("## Analysis for FO stocks at 9:10 AM Using Pre-Open market")
    st.markdown("### CE Buy Oppourtunities")
    df_ce_buy_opp = printAnalysis(f_preeopen_buy_opp_df)
    st.table(df_ce_buy_opp)
    
    st.markdown("### PE Buy Oppurtunities")
    preopen_loosers_df = preeopen_df.tail(10).sort_values(['pChange'], ascending=True)
    df_pe_buy_opp = printAnalysis(preopen_loosers_df)
    st.table(df_pe_buy_opp) 
    elapsed = time.time() - start
    print("Programme Took Total of :-" + str(elapsed))
    # gb = GridOptionsBuilder.from_dataframe(df)
    # gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    # gb.configure_selection(selection_mode='single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    
    # gb.configure_grid_options(domLayout='normal')
    # gridOptions = gb.build()
    
    # grid_response = AgGrid(
    #     df, 
    #     gridOptions=gridOptions,
    #     width='100%',
    #     data_return_mode='FILTERED_AND_SORTED', 
    #     fit_columns_on_grid_load=False,
    #     allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    #     enable_enterprise_modules=False
    # )
    # st.write(grid_response['selected_rows'])
    # return grid_response

app()

