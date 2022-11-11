# pip install pandas
# pip install numpy
# pip install smartapi-python
# pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl

from smartapi import SmartConnect
import document_detail_Lax
import time
import datetime
import talib as ta
import pandas as pd
import numpy as np
import sys
import pyotp

api_key = document_detail_Lax.api_key
secret_key = document_detail_Lax.secret_key
user_id = document_detail_Lax.user_id
password = document_detail_Lax.password
totp_token = document_detail_Lax.totp_token 

script_list = {
    "MARUTI-EQ": "10999",
    "LALPATHLAB-EQ": "11654",
    "IDFCFIRSTB-EQ": "11184",
    "CONCOR-EQ": "4749",
    "PEL-EQ": "2412",
    "MUTHOOTFIN-EQ": "23650",
    "ESCORTS-EQ": "958",
    "PIDILITIND-EQ": "2664",
    "JSWSTEEL-EQ": "11723",
    "ACC-EQ": "22",
    "SAIL-EQ": "2963",
    "ICICIPRULI-EQ": "18652",
    "GRASIM-EQ": "1232",
    "ASTRAL-EQ": "14418",
    "BHARATFORG-EQ": "422",
    "ATUL-EQ": "263",
    "IPCALAB-EQ": "1633",
    "BEL-EQ": "383",
    "PNB-EQ": "10666",
    "HDFCLIFE-EQ": "467",
    "NATIONALUM-EQ": "6364",
    "DELTACORP-EQ": "15044",
    "UPL-EQ": "11287",
    "APOLLOHOSP-EQ": "157",
    "CIPLA-EQ": "694",
    "WHIRLPOOL-EQ": "18011",
    "DALBHARAT-EQ": "8075",
    "INFY-EQ": "1594",
    "FEDERALBNK-EQ": "1023",
    "ALKEM-EQ": "11703",
    "AMBUJACEM-EQ": "1270",
    "TITAN-EQ": "3506",
    "OBEROIRLTY-EQ": "20242",
    "CUMMINSIND-EQ": "1901",
    "NMDC-EQ": "15332",
    "SUNPHARMA-EQ": "3351",
    "ADANIENT-EQ": "25",
    "LTTS-EQ": "18564",
    "PIIND-EQ": "24184",
    "CHOLAFIN-EQ": "685",
    "BHEL-EQ": "438",
    "MFSL-EQ": "2142",
    "M&MFIN-EQ": "13285",
    "LUPIN-EQ": "10440",
    "GUJGASLTD-EQ": "10599",
    "SUNTV-EQ": "13404",
    "ICICIGI-EQ": "21770",
    "STAR-EQ": "7374",
    "PVR-EQ": "13147",
    "GRANULES-EQ": "11872",
    "MCX-EQ": "31181",
    "INDHOTEL-EQ": "1512",
    "SBICARD-EQ": "17971",
    "M&M-EQ": "2031",
    "PFIZER-EQ": "2643",
    "INDUSTOWER-EQ": "29135",
    "VEDL-EQ": "3063",
    "BALKRISIND-EQ": "335",
    "SIEMENS-EQ": "3150",
    "HAVELLS-EQ": "9819",
    "DRREDDY-EQ": "881",
    "BERGEPAINT-EQ": "404",
    "IOC-EQ": "1624",
    "LT-EQ": "11483",
    "BANKBARODA-EQ": "4668",
    "DABUR-EQ": "772",
    "LAURUSLABS-EQ": "19234",
    "FSL-EQ": "14304",
    "TORNTPOWER-EQ": "13786",
    "GMRINFRA-EQ": "13528",
    "MARICO-EQ": "4067",
    "INDIACEM-EQ": "1515",
    "EICHERMOT-EQ": "910",
    "BANDHANBNK-EQ": "2263",
    "GODREJPROP-EQ": "17875",
    "BHARTIARTL-EQ": "10604",
    "BPCL-EQ": "526",
    "NAUKRI-EQ": "13751",
    "HINDALCO-EQ": "1363",
    "ITC-EQ": "1660",
    "POLYCAB-EQ": "9590",
    "CADILAHC-EQ": "7929",
    "SBILIFE-EQ": "21808",
    "DIXON-EQ": "21690",
    "HEROMOTOCO-EQ": "1348",
    "TATAPOWER-EQ": "3426",
    "ICICIBANK-EQ": "4963",
    "SBIN-EQ": "3045",
    "HINDPETRO-EQ": "1406",
    "POWERGRID-EQ": "14977",
    "ABFRL-EQ": "30108",
    "LICHSGFIN-EQ": "1997",
    "TRENT-EQ": "1964",
    "TVSMOTOR-EQ": "8479",
    "DIVISLAB-EQ": "10940",
    "GODREJCP-EQ": "10099",
    "GAIL-EQ": "4717",
    "MINDTREE-EQ": "14356",
    "BAJAJFINSV-EQ": "16675",
    "VOLTAS-EQ": "3718",
    "APLLTD-EQ": "25328",
    "DEEPAKNTR-EQ": "19943",
    "TATACONSUM-EQ": "3432",
    "HINDUNILVR-EQ": "1394",
    "ULTRACEMCO-EQ": "11532",
    "ASIANPAINT-EQ": "236",
    "CANBK-EQ": "10794",
    "EXIDEIND-EQ": "676",
    "IEX-EQ": "220",
    "JUBLFOOD-EQ": "18096",
    "CHAMBLFERT-EQ": "637",
    "HDFC-EQ": "1330",
    "WIPRO-EQ": "3787",
    "L&TFH-EQ": "24948",
    "MOTHERSUMI-EQ": "4204",
    "INDUSINDBK-EQ": "5258",
    "COLPAL-EQ": "15141",
    "CANFINHOME-EQ": "583",
    "HDFCAMC-EQ": "4244",
    "NTPC-EQ": "11630",
    "HAL-EQ": "2303",
    "UBL-EQ": "16713",
    "SRF-EQ": "3273",
    "BRITANNIA-EQ": "547",
    "NESTLEIND-EQ": "17963",
    "TATAMOTORS-EQ": "3456",
    "BAJFINANCE-EQ": "317",
    "OFSS-EQ": "10738",
    "JKCEMENT-EQ": "13270",
    "TORNTPHARM-EQ": "3518",
    "INDIGO-EQ": "11195",
    "PFC-EQ": "14299",
    "PAGEIND-EQ": "14413",
    "CUB-EQ": "5701",
    "MANAPPURAM-EQ": "19061",
    "LTI-EQ": "17818",
    "AUBANK-EQ": "21238",
    "MRF-EQ": "2277",
    "COFORGE-EQ": "11543",
    "METROPOLIS-EQ": "9581",
    "TATACHEM-EQ": "3405",
    "BOSCHLTD-EQ": "2181",
    "IBULHSGFIN-EQ": "30125",
    "RAMCOCEM-EQ": "2043",
    "ZEEL-EQ": "3812",
    "SYNGENE-EQ": "10243",
    "RECLTD-EQ": "15355",
    "TATASTEEL-EQ": "3499",
    "COROMANDEL-EQ": "739",
    "CROMPTON-EQ": "17094",
    "AUROPHARMA-EQ": "275",
    "AXISBANK-EQ": "5900",
    "RBLBANK-EQ": "18391",
    "PETRONET-EQ": "11351",
    "JINDALSTEL-EQ": "6733",
    "GLENMARK-EQ": "7406",
    "KOTAKBANK-EQ": "1922",
    "GSPL-EQ": "13197",
    "ADANIPORTS-EQ": "15083",
    "COALINDIA-EQ": "20374",
    "AMARAJABAT-EQ": "100",
    "TCS-EQ": "11536",
    "ONGC-EQ": "2475",
    "APOLLOTYRE-EQ": "163",
    "BIOCON-EQ": "11373",
    "PERSISTENT-EQ": "18365",
    "DLF-EQ": "14732",
    "SRTRANSFIN-EQ": "4306",
    "MPHASIS-EQ": "4503",
    "NAVINFLUOR-EQ": "14672",
    "INDIAMART-EQ": "10726",
    "MGL-EQ": "17534",
    "IRCTC-EQ": "13611",
    "IGL-EQ": "11262",
    "BSOFT-EQ": "6994",
    "BATAINDIA-EQ": "371",
    "HCLTECH-EQ": "7229",
    "SHREECEM-EQ": "3103",
    "RELIANCE-EQ": "2885",
    "HDFCBANK-EQ": "1333",
    "TECHM-EQ": "13538",
    "ASHOKLEY-EQ": "212"
}
buy_traded_stock = []
sell_traded_stock = []
exchange = "NSE"
supertrend_period = 30
supertrend_multiplier = 3
runcount = 0


def GettingMargin():
    margin = obj.rmsLimit()["data"]["availablecash"]
    no_of_trade = 10
    per_trade_fund = int(int(margin) / no_of_trade)
    return per_trade_fund


def GettingLtpData(script, token, order):
    LTP = obj.ltpData(exchange, script, token)
    ltp = LTP["data"]["ltp"]
    quantity = int(GettingMargin() / ltp)
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": script,
        "symboltoken": token,
        "transactiontype": order,
        "exchange": exchange,
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": ltp,
        "squareoff": "0",
        "stoploss": "0",
        "quantity": quantity
    }
    orderId = None # obj.placeOrder(orderparams)
    print(
        f"{order} order Place for {script} with quantity {ltp}: {quantity} at : {datetime.datetime.now()} with Order id {orderId}"
    )


def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat(
        [df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def ATR(df, period, ohlc=['open', 'high', 'low', 'close']):
    """
    Function to compute Average True Range (ATR)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = 'ATR_' + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not 'TR' in df.columns:
        df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
        df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

        df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

        df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, 'TR', atr, period, alpha=True)

    return df


def SuperTrend(df,
               period=supertrend_period,
               multiplier=supertrend_multiplier,
               ohlc=['open', 'high', 'low', 'close']):
    """
    Function to compute SuperTrend
    
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
        
    Returns :
        df : Pandas DataFrame with new columns added for 
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST'
    stx = 'STX'
    """
    SuperTrend Algorithm :
    
        BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
        BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
        
        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                            THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
        
        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LOWERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                    Current FINAL UPPERBAND
    """

    # Compute basic upper and lower bands
    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    # Compute final upper and lower bands
    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[
            i] < df['final_ub'].iat[i - 1] or df[ohlc[3]].iat[
                i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i -
                                                                           1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[
            i] > df['final_lb'].iat[i - 1] or df[ohlc[3]].iat[
                i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i -
                                                                           1]

    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
                        df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] >  df['final_ub'].iat[i] else \
                        df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
                        df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] <  df['final_lb'].iat[i] else 0.00

    # Mark the trend direction up/down
    df[stx] = np.where((df[st] > 0.00),
                       np.where((df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)

    # Remove basic and final bands from the columns
    df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'],
            inplace=True,
            axis=1)

    df.fillna(0, inplace=True)
    return df


def strategy():
    global obj

    obj = SmartConnect(api_key=api_key)
    # token = obj.generateToken(obj.generateSession(user_id, password)["data"]["refreshToken"])
    # jwtToken = token['data']["jwtToken"]
    # refreshToken = token['data']['refreshToken']
    # feedToken = token['data']['feedToken']
    data = obj.generateSession(user_id, password, pyotp.TOTP(totp_token).now())
    token= data['data']['refreshToken']
    jwtToken = data['data']['jwtToken']
    feedToken=obj.getfeedToken()

    fromdate = "2022-08-01 09:15" # The difference between Fromdate to Todate should not be more than 100 days;
    todate = f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")[:-1]}5'

    try:
        for script, token in script_list.items():
            historicParam = {
                "exchange": exchange,
                "symboltoken": token,
                "interval": "FIFTEEN_MINUTE",
                "fromdate": fromdate,
                "todate": todate
            }
            hist_data = obj.getCandleData(historicParam)["data"]
            if hist_data != None:
                df = pd.DataFrame(
                    hist_data,
                    columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                df = SuperTrend(df)
                df.dropna(inplace=True)
                if not df.empty:
                    super_trend = df.STX.values
                    if (super_trend[-1] == 'down' and super_trend[-2] == 'up'
                            and super_trend[-3] == 'up'
                            and super_trend[-4] == 'up'
                            and super_trend[-5] == 'up') and (script not in sell_traded_stock):
                        sell_traded_stock.append(script)
                        GettingLtpData(script, token, "SELL")

                    if (super_trend[-1] == 'up' and super_trend[-2] == 'down'
                            and super_trend[-3] == 'down'
                            and super_trend[-4] == 'down'
                            and super_trend[-5] == 'down') and (script not in buy_traded_stock):
                        buy_traded_stock.append(script)
                        GettingLtpData(script, token, "BUY")

    except Exception as e:
        print(e)

    try:
        logout = obj.terminateSession(user_id)
        print("Logout Successfull")
    except Exception as e:
        print(e)


def main():
    global runcount

    start_time = int(9) * 60 + int(20)
    end_time = int(15) * 60 + int(10)
    stop_time = int(15) * 60 + int(15)
    last_time = start_time
    schedule_interval = 60 * 10

    while True:
        if (datetime.datetime.now().hour * 60 +
                datetime.datetime.now().minute) >= end_time:
            if (datetime.datetime.now().hour * 60 +
                    datetime.datetime.now().minute) >= stop_time:
                print(sys._getframe().f_lineno,
                      "Trading is closed, time is above 03:15 PM")
                break

        elif (datetime.datetime.now().hour * 60 +
              datetime.datetime.now().minute) >= start_time:
            if time.time() >= last_time:
                last_time = time.time() + schedule_interval
                print(
                    f"{runcount} Run Count : Time - {datetime.datetime.now()}")
                if runcount >= 0:
                    try:
                        strategy()
                    except Exception as e:
                        print(e)
                runcount = runcount + 1
        else:
            print(f'Waiting...strategy will start working at 09:20 AM')
            time.sleep(1)


if (__name__ == '__main__'):
    main()