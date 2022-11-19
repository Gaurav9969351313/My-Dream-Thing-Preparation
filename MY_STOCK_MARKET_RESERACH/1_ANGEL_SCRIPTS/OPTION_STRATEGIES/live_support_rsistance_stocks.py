
import requests
import json
import math

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
    response = sess.get(url_oc, headers=headers, timeout=5, cookies=cookies)
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""

def print_oi(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                #print((str(item["strikePrice"])) + (" CE ") + "[ " + (str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + (" PE ")+"[ " + (str(item["PE"]["openInterest"]).rjust(10," ")) + " ]")
                print(data["records"]["expiryDates"][0] + " " + str(item["strikePrice"]) + 
                      " CE " + "[ " + (str(item["CE"]["openInterest"]).rjust(10," ")) + " ]"
                      + " COI: "+ (str(item["CE"]["changeinOpenInterest"])).rjust(10," ") + "" + 
                      " PE " + "[ " + (str(item["PE"]["openInterest"]).rjust(10," ")) + " ]"
                      + " COI: "+ (str(item["CE"]["changeinOpenInterest"])).rjust(10," ") +"" )
                strike = strike + step
                
    return data
                
                

# Finding highest Open Interest of People's in CE based on CE data         
def highest_oi_CE(num,step,nearest,url, data):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    # response_text = get_data(url)
    # data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["CE"]["openInterest"] > max_oi:
                    max_oi = item["CE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

# Finding highest Open Interest of People's in PE based on PE data 
def highest_oi_PE(num,step,nearest,url, data):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    # response_text = get_data(url)
    # data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["PE"]["openInterest"] > max_oi:
                    max_oi = item["PE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

num=12
step=20
atm_strike = 3320
symbol = "TCS"
f_url = url_eq+ symbol

data = print_oi(num,step, atm_strike, f_url)
print((str("Major Support in " +symbol + ": ")) + str(highest_oi_CE(num,step,atm_strike, f_url, data)))
print((str("Major Resistance in " +symbol + ": ")) + str(highest_oi_PE(num,step,atm_strike, f_url, data)))