from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import parameters, csv, os.path, time
from selenium.webdriver.common.by import By
import re
import random
from fake_useragent import UserAgent

query = '"Headhunter" "@gmail.com" AND "Berlin" site:linkedin.com'

file_name = "hr.csv"
file_exists =  os.path.isfile(file_name)
writer = csv.writer(open(file_name, 'a'))
if not file_exists: writer.writerow(['email'])

for i in range(0,300,10):  
    ri = random.randint(1,5)
    print(ri)
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_extension('./buster.crx')
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--incognito --disable-blink-features=AutomationControlled");
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver.profile.set_preference("security.fileuri.strict_origin_policy", False)
    # time.sleep(30)
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get('https://www.google.com/search?q='+ query + '&start=' + str(i)) 
        s = driver.find_element_by_id('main').text
        # append s in text file 
        emails = re.findall(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+', s)
        time.sleep(ri)
        for e in emails:
            writer.writerow([e])
            print(e)
    # print("Page No: "+ str(i) +") =================================")
    except:
        captcha = driver.find_element_by_class_name('g-recaptcha')
        site_key = captcha.get_attribute('data-sitekey')
        print("Site Key:- " + site_key)
        time.sleep(20)
        driver.close()



    
    
 