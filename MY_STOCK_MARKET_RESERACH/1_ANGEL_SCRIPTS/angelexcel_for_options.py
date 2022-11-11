from smartapi import SmartConnect, SmartWebSocket
import document_detail_Lax
import time
import datetime
import talib as ta
import xlwings as xw
import pandas as pd
import pyotp
import json

totp_token = document_detail_Lax.totp_token 
api_key = document_detail_Lax.api_key
secret_key = document_detail_Lax.secret_key
user_id = document_detail_Lax.user_id
password = document_detail_Lax.password

exchange = "NSE"
sheet = xw.Book("E:/ANGEL_SCRIPTS/angel_trade_setup.xlsx").sheets[1]

script_list = {
    'BANKNIFTY27OCT2240200CE':'57191',
    'BANKNIFTY27OCT2240600PE':'57200',
    'BANKNIFTY27OCT2240000CE':'57187',
    'BANKNIFTY27OCT2240700CE':'57201',
    'BANKNIFTY27OCT2240900PE':'57206',
    'BANKNIFTY27OCT2240600CE':'57199',
    'BANKNIFTY27OCT2240900CE':'57205',
    'BANKNIFTY27OCT2240100PE':'57190',
    'BANKNIFTY27OCT2240000PE':'57188',
    'BANKNIFTY27OCT2240500PE':'57198',
    'BANKNIFTY27OCT2240400PE':'57196',
    'BANKNIFTY27OCT2240700PE':'57202',
    'BANKNIFTY27OCT2240200PE':'57192',
    'BANKNIFTY27OCT2240100CE':'57189',
    'BANKNIFTY27OCT2240300PE':'57194',
    'BANKNIFTY27OCT2240300CE':'57193',
    'BANKNIFTY27OCT2240500CE':'57197',
    'BANKNIFTY27OCT2240400CE':'57195',
    'BANKNIFTY27OCT2240800CE':'57203',
    'BANKNIFTY27OCT2240800PE':'57204'

}

sheet.range("B1:M300").clear_contents()
tickerlist = sheet.range("A2").expand("down").value
buy_traded_stocks = []
sell_traded_stocks = []

data = {}
def name(token, ltp):
    for i, j in script_list.items():        
        if (j == token) and (i not in data):
            return i
        if (j == token) and (i in data):
            return i

def sendData(message):
    sheet = xw.Book("E:/ANGEL_SCRIPTS/angel_trade_setup.xlsx").sheets[1]
    dataDict = message[0] 
    ltp = message[0]["ltp"]
    token = message[0]["tk"]
    prev_close = message[0]["c"]
    change = message[0]["cng"]
    netChange = message[0]["nc"]
    
    sheet.range("A1").value = [
        "Script", "Token", "Ltp", "Prev Close", "Change", "netChange",
        "Condition", "Order_Type", "Quantity", "Order_Status"
    ]
    script_name = name(token, ltp)
    cell_no = 0
    for i in tickerlist:
        if i != None:
            if i.upper() == script_name:
                cell_no = tickerlist.index(i) + 2

    sheet.range(f"B{cell_no}").value = token
    if ltp != None:
        sheet.range(f"C{cell_no}").value = ltp
    sheet.range(f"D{cell_no}").value = prev_close
    sheet.range(f"E{cell_no}").value = change
    sheet.range(f"F{cell_no}").value = netChange

def socketOpen(task, token, feedToken, user_id):
    ss = SmartWebSocket(feedToken, user_id)

    def on_message(ws, message):
        print(message[0])
        sendData(message)
        print("==================================")

    def on_open(ws):
        ss.subscribe(task, token)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("Close")

    # Assign the callbacks.
    ss._on_open = on_open
    ss._on_message = on_message
    ss._on_error = on_error
    ss._on_close = on_close

    ss.connect()



def main():
    global obj

    obj = SmartConnect(api_key=api_key)  
    data = obj.generateSession(user_id, password, pyotp.TOTP(totp_token).now())
    refreshToken= data['data']['refreshToken']
    jwtToken = data['data']['jwtToken']
    feedToken=obj.getfeedToken()

    empty = []
    for i in tickerlist:
        if i != None:
            i = f"{i.upper()}"
            if i in script_list:
                empty.append(f"nse_fo|{script_list[i]}&")
    newS = "".join([i for i in empty])
    token = newS[:-1]

    task = "mw"
    socketOpen(task, token, feedToken, user_id)

if (__name__ == '__main__'):
    main()