from io import BytesIO
import os
import telebot
import yfinance as yf
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import talib
import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
from datetime import date
from tradingview_ta import TA_Handler, Interval, Exchange
from matplotlib.backends.backend_pdf import PdfPages
import requests

pd.set_option('display.max_colwidth', None)
AVERAGE_FACTOR = 22

PERIOD_LIST = ['1d','7d','max']
INTERVAL = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'] 
TICKER_LIST = ['ITC.NS', 'BAJFINANCE.NS','BAJAJFINSV.NS','SILVERBEES.NS','DELTACORP.NS','DMART.NS','COALINDIA.NS','DEEPAKNTR.NS','BHARTIARTL.NS','HDFC.NS','IOC.NS', 'HDFCBANK.NS', 'AARTIIND.NS', 'UPL.NS', 'ASIANPAINT.NS', 'AFFLE.NS', 'PIDILITIND.NS', 'INFY.NS','LT.NS','DIXON.NS', 'HAL.NS']
ETF_TICKER_LIST = ['NIFTYBEES.NS', 'BANKBEES.NS', 'ITBEES.NS', 'GOLDBEES.NS', 'JUNIORBEES.NS', 'SILVERBEES.NS'] 

MF_SCHEME_CODE = [
    {"schemecode": 122639, "name": "Parag Parekh Flexi Cap Regular"},
    {"schemecode": 125350, "name": "Axis Small Cap Fund - Regular Plan - Growth"},
    {"schemecode": 102875, "name": "Kotak-Small Cap Fund - Growth"},
    {"schemecode": 135799, "name": "TATA Digital India Fund Regular Plan"},
    {"schemecode": 112090, "name": "Kotak Flexicap Fund Regular"},
    {"schemecode": 120841, "name": "quant Mid Cap Fund - Growth Option - Direct"}
]

def getHistoricalMFNavData(schemeCode):
    url = "https://api.mfapi.in/mf/"+str(schemeCode) 
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data = response.json()
        df = pd.DataFrame(data['data'])
        dfToConsider = df.head(AVERAGE_FACTOR)
        return dfToConsider
    else:
        return None


def getData(ticker_list, period_index, interval_index):
    df = yf.download(tickers = ticker_list, period = PERIOD_LIST[period_index], interval = INTERVAL[interval_index], 
                                    auto_adjust = True, prepost = True, threads = True, proxy = None).reset_index()
    return df

def getIndicatorValues(y_ticker_name):
    ticker = y_ticker_name.replace(".NS", "")
    ticker = y_ticker_name.replace("&", "_")
    indicator_values = TA_Handler(
        symbol=ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_DAY
    )

    df1 = pd.DataFrame([indicator_values.get_analysis().indicators])
    df2 = pd.DataFrame([indicator_values.get_analysis().summary])
    df = pd.concat([df1, df2], axis=1, join='inner')
    
    df_i = df[['RECOMMENDATION', 'BUY', 'SELL', 'NEUTRAL', 'RSI', 'open', 'low', 'high', 'change', 'volume', 'RSI[1]','ADX','Stoch.K', 'Stoch.D', 'AO[2]','UO','MACD.macd', 'MACD.signal', 'Stoch.K', 'Stoch.D', 'Stoch.K[1]', 'Stoch.D[1]','EMA50', 'SMA50',  'Rec.VWMA', 'VWMA']]
    return df_i

def getPortfolioData(ticker_list):
    data_arr = []
    indicator_dfs = []
    for ticker in ticker_list:
        ticker_data_obj = {}
        data_df = getData(ticker, 1, 8)
        ticker_data_obj["ticker_name"] = ticker
        ticker_data_obj["data_df"] = data_df
        indicator_df = getIndicatorValues(ticker)
        indicator_df["ticker"] = ticker
        
        indicator_df_columns = indicator_df.columns.tolist()
        indicator_df_columns.insert(0, "ticker")
        
        new_indicator_df = indicator_df[indicator_df_columns]
        indicator_dfs.append(new_indicator_df)
        data_arr.append(ticker_data_obj)
    return data_arr, indicator_dfs


API_KEY = '5711438740:AAFq_RSfXkytoOfYiYBOvRbhC5YJKtIbJrM'

updater = Updater(API_KEY,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /pia   :- Stocks Portfolio Indicator Analysis                          
    /mfa   :- Mutual Fund Portfolio Analysis
    /etfia :- ETF Indicator Analysis                          
    /ryc   :- Rental Yeild Calculator 
              Ex: /ryc monthly_rent|monthly_maintainance|property_value
    """)
  
def rental_yeild_calculator(update: Update, context: CallbackContext):
    input = str(update.message.text.replace("/ryc", ""))    
    arr = input.split("|")
    monthly_rental_income = float(arr[0])
    monthly_maintainance = float(arr[1])
    property_value = float(arr[2])
    result = round((((monthly_rental_income * 12) - (monthly_maintainance * 12)) / property_value) * 100, 3)
    update.message.reply_text(result)
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
    
def get_portfolio_analysis(update: Update, context: CallbackContext):
    arr, ind_dfs = getPortfolioData(TICKER_LIST)
    final_indicator_df = pd.concat(ind_dfs)
    colors = []
    for _, row in final_indicator_df.iterrows():
        colors_in_column = ["w", "w","w","w", "w","w","w", 
                            "w", "w","w","w", "w","w","w", 
                            "w", "w","w","w", "w","w","w",
                            "w", "w","w","w", "w","w","w",
                            "w", "w","w","w"]
        if row["RSI"] < 35:
            colors_in_column[5] = "g"
        if row["RSI"] > 60:
            colors_in_column[5] = "r"
        colors.append(colors_in_column)

    fig, ax =plt.subplots(figsize=(22,10))
    ax.axis('tight')
    ax.axis('off')
    today = date.today()
    the_table = ax.table(cellText=final_indicator_df.values,colLabels=final_indicator_df.columns,loc='left',  cellColours=colors)
    pp = PdfPages("PF-" + str(today) + ".pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    
    chat_id = update.message.chat_id
    document = open("./PF-" + str(today) + ".pdf", 'rb')
    context.bot.send_document(chat_id, document)
    
def get_mf_analysis(update: Update, context: CallbackContext):
    today = date.today()
    pdf = PdfPages("MF-" + str(today) + ".pdf")
    for x in MF_SCHEME_CODE:
        dfC = getHistoricalMFNavData(x["schemecode"])
        dfC['nav'] = dfC['nav'].astype(float)

        dfC_columns = dfC.columns.tolist()
        dfC_columns.insert(0, "name")
        dfC['name'] = x['name']
        new_df = dfC[dfC_columns]
        
        fig, ax =plt.subplots(figsize=(8,8))
        ax.axis('tight')
        ax.axis('off')
        ax.set_title(x['name'])
        the_table = ax.table(cellText=new_df.values,colLabels=new_df.columns,loc='left')
        pdf.savefig(fig, bbox_inches='tight')
    pdf.close()  
    chat_id = update.message.chat_id
    document = open("./MF-" + str(today) + ".pdf", 'rb')
    context.bot.send_document(chat_id, document)
        
def get_etf_analysis(update: Update, context: CallbackContext):
    today = date.today()
    pdf = PdfPages("ETF-" + str(today) + ".pdf")
    arr, ind_dfs = getPortfolioData(ETF_TICKER_LIST)
    final_indicator_df = pd.concat(ind_dfs)
    fig, ax =plt.subplots(figsize=(22,12))
    ax.axis('tight')
    ax.axis('off')
    today = date.today()
    the_table = ax.table(cellText=final_indicator_df.values,colLabels=final_indicator_df.columns,loc='left')
    pdf.savefig(fig, bbox_inches='tight')
    
    for a in arr:
        ax.set_title(a['ticker_name'])
        ax.table(cellText=a['data_df'].values,colLabels=a['data_df'].columns,loc='left')
        pdf.savefig(fig, bbox_inches='tight')
        
    pdf.close()
    
    chat_id = update.message.chat_id
    document = open("./ETF-" + str(today) + ".pdf", 'rb')
    context.bot.send_document(chat_id, document)
    
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('ryc', rental_yeild_calculator))
updater.dispatcher.add_handler(CommandHandler('pia', get_portfolio_analysis))
updater.dispatcher.add_handler(CommandHandler('mfa', get_mf_analysis))
updater.dispatcher.add_handler(CommandHandler('etfia', get_etf_analysis))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
  
updater.start_polling()