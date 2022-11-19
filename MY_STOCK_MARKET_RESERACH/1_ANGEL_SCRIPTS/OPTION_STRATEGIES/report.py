
import requests
import json
import math
from nsepython import * 

url_oc      = "https://www.nseindia.com/option-chain"
url_eq = "https://www.nseindia.com/api/option-chain-equities?symbol="

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    
def get_data(url):
    set_cookie()
    payload = nsefetch(url)
    return payload
    
    # response = sess.get(url_oc, headers=headers, timeout=5, cookies=cookies)
    # set_cookie()
    # response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    # if(response.status_code==200):
    #     return response.text
    # return ""


def getOIInterPretation(lp_change, coi):
    oi_intrepretation = ""
    if(lp_change>0 and coi>0):
        oi_intrepretation = "Long Buildup"
    if(lp_change>0 and coi<0):
        oi_intrepretation = "Short covering"
    if(lp_change<0 and coi<0):
       oi_intrepretation = "Long Liquidation"
    if(lp_change<0 and coi>0):
       oi_intrepretation = "Short Buildup"
    return oi_intrepretation

def print_oi(num,url):
    data = get_data(url)
    # data = json.loads(response_text)
    step = data['records']['strikePrices'][1] - data['records']['strikePrices'][0]
    option_chain_data = data['records']['data']
    ltp = option_chain_data[0]['PE']['underlyingValue']
    strike_price_list = [x['strikePrice'] for x in option_chain_data]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    nearest = atm_strike
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    currExpiryDate = data["records"]["expiryDates"][0]
    
    oi_interpreted = []
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                obj = {}
                
                obj["ce_oi"] = int(item["CE"]["openInterest"])
                obj["ce_coi"] = float(item["CE"]["changeinOpenInterest"])
                obj["ce_lp"] = float(item["CE"]["lastPrice"])
                obj["ce_lp_change"] = float(item["CE"]["change"])
                obj["ce_oi_inteerpretation"] = getOIInterPretation(obj["ce_lp_change"], obj["ce_coi"])
                obj["strikePrice"] = str(item["strikePrice"])
                obj["pe_lp_change"] = float(item["PE"]["change"])
                obj["pe_oi"] = int(item["PE"]["openInterest"])
                obj["pe_coi"] = float(item["PE"]["changeinOpenInterest"])
                obj["pe_lp"] = float(item["PE"]["lastPrice"])
                obj["pe_oi_inteerpretation"] = getOIInterPretation(obj["pe_lp_change"], obj["pe_coi"])
                oi_interpreted.append(obj)
                # print((str(item["strikePrice"])) + (" CE ") + "[ " + (str(item["CE"]["openInterest"]).rjust(30," ")) + " " + obj["ce_oi_inteerpretation"] + " ]" + 
                                                #    (" PE ") + "[ " + (str(item["PE"]["openInterest"]).rjust(30," ")) + " " + obj["pe_oi_inteerpretation"] + " ]")
                strike = strike + step
    return oi_interpreted

def getCETrend(sum_coi_ce, sum_coi_pe):
    if(sum_coi_ce > sum_coi_pe):
        return "BEARISH"
    elif (sum_coi_ce < sum_coi_pe):
        return "BULLISH"

def afterAnalysis(fdf): 
   
    sum_coi_ce = fdf["ce_coi"].sum()
    sum_coi_pe = fdf["pe_coi"].sum()

    sum_lpc_ce = fdf["ce_lp_change"].sum()
    sum_lpc_pe = fdf["pe_lp_change"].sum()

    def getIntraDayTrend(sum_coi_ce, sum_coi_pe):
        if(sum_coi_ce > sum_coi_pe):
            return "BEARISH"
        elif (sum_coi_ce < sum_coi_pe):
            return "BULLISH"
        
    intra_day_trend = getIntraDayTrend(sum_coi_ce, sum_coi_pe)
    overall_trend = getIntraDayTrend(sum_lpc_pe, sum_lpc_ce)

    print(intra_day_trend)
    print(overall_trend)
    
oi_interpreted = print_oi(10, url_eq+ "INFY")
fdf = pd.DataFrame(oi_interpreted)
afterAnalysis(fdf)

print(fdf[["ce_oi_inteerpretation", "ce_lp", "strikePrice","pe_lp","pe_oi_inteerpretation"]])