import pandas as pd
import requests
from bs4 import BeautifulSoup
import errno
import os
import numpy as np
import matplotlib.pyplot as plt
from urllib.parse import quote_plus, urlencode
from time import  sleep
from datetime import  datetime

import six

all_scanners = []
bot_token =None
bot_chatID = None

link = "https://chartink.com/screener/"
url = 'https://chartink.com/screener/process'
interval_seconds = 10
previous_scan_results = set()


scanner_filename = "./saha/scanner.txt"
bot_filename = "./saha/bot_det.txt"
if not os.path.exists(os.path.dirname(scanner_filename)):
    try:
        os.makedirs(os.path.dirname(scanner_filename))
        print("look for folder saha, inside two files are availabe. chage accordingly")
        print("replace only scan_clause: formula")
        print("replease bot_id and chat_id with your details")

        with open( scanner_filename,'w') as f:
            f.writelines(["scan_clause:( {33492} ( [=1] 15 minute close > [=1] 15 minute upper bollinger band( 20 , 2 ) and [=1] 15 minute close > [=1] 15 minute open and [=2] 15 minute close < [=2] 15 minute open and [=2] 15 minute close < [=2] 15 minute vwap ) )","\n","every_n_seconds:30"])
        with open( bot_filename,'w') as f:
            f.writelines(["bot_id","\n","chat_id"])
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
    exit(0)


for filename in os.listdir('./saha'):
    if 'scanner.txt' in filename:
        with open(scanner_filename, 'r') as f: # open in readonly mode
           lns = f.readlines()
           all_scanners.append(lns[0].split("scan_clause:"))
           interval_seconds = int(lns[1].split("every_n_seconds:")[1])
    if 'bot_det.txt'in filename:
        with open(bot_filename, 'r') as f:
            lns = f.readlines()
            bot_token = lns[0].strip()
            bot_chatID = lns[1].strip()


if bot_chatID is None or bot_token is None:
    print("crate file with bot_det.txt in saha\bot_det.txt and two lines. first line with token, second line with bot chatid")
    exit(0)

if len(all_scanners) ==0:
    print('create chart link files in saha folder and then run script again. first line url')

def send_telegrms_msg(message):
        # add your channel ID or group id
        data = {
            'text': message,
            'chat_id': int(bot_chatID),
            'parse_mode': 'MARKDOWN'
        }
        encodedData = urlencode(data, quote_via=quote_plus)

        url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?' + encodedData
        response = requests.get(url)
        return response.json()


def send_telegrms_photo(filename):
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        files = {}
        files["photo"] = open(filename, "rb")
        requests.get(url, params={"chat_id": bot_chatID}, files=files)



def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                         header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                         bbox=[0, 0, 1, 1], header_columns=0,
                         ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])
        return ax, fig



while True:

    print(f"scanning chart scanner...... {datetime.now()}")
    for scanner in all_scanners:
        formula = scanner[1]
        payload = {
            'scan_clause': formula
        }

        link = "https://chartink.com/screener/"
        url = 'https://chartink.com/screener/process'

        with requests.Session() as s:
            r = s.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            csrf = soup.select_one("[name='csrf-token']")['content']
            s.headers['x-csrf-token'] = csrf
            print(payload['scan_clause'])
            r = s.post(url, data=payload)
            df = pd.DataFrame(columns=['sr', 'nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume'], index=None)
            print(df.columns)

            '''for item in r.json()['data']:
                df = df.append(item, ignore_index=True)
            '''
            data = r.json()['data']
            df = None
            if len(data) > 0:
                df = pd.DataFrame(r.json()['data'])
                df.index = df['sr']
                df.drop('sr', axis=1, inplace=True)
                del df['name']


        if df is not None and df.shape[0]>0:
                print(df)
                df.to_csv('chartink.csv')
        else:
            print('no results found')

        strng = None

        if df is not None and df.shape[0]>0:
            print(f'results found {df.shape[0]}')
            strng = '_______________________________________________\n'
            strng = strng + '{:20s} {:15s} {:20s} '.format("STOCK", "CLOSE", "PCT_CHNG") + "\n"
            strng = strng + '_______________________________________________\n'
            for index, row in df.iterrows():
                strng = strng + '{:20s} {:15} {:5s} '.format(row['nsecode'], str(row['close']), str(row['per_chg'])) + "\n"
            strng = strng + '______________________________________________\n'
            print(strng)

        if df is not None and df.shape[0]>0:
            strng = ""

            for index, row in df.iterrows():
                if row['nsecode'] not in previous_scan_results:
                    strng = strng + f"{row['nsecode']}, {str(row['close'])}, {str(row['per_chg'])}" + "\n"
                    previous_scan_results.add(row['nsecode'])
            if len(strng)>0:
                print(send_telegrms_msg(strng))
            else:
                print('No new reulst found, not sending telegrm msg')

        print(f'{interval_seconds} <<== seconds waiting')
        sleep(interval_seconds)
