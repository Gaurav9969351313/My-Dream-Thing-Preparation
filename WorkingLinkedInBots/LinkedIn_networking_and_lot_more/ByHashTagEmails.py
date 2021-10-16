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

options = Options()
# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)
# options.add_argument(f'user-agent={userAgent}')
options.add_extension('./emailextractor.crx')
# options.add_argument("start-maximized")
# options.add_argument('disable-infobars')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--incognito --disable-blink-features=AutomationControlled");

def scrollit(tagName, options):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # 
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys(parameters.linkedin_username)
        driver.find_element_by_id('password').send_keys(parameters.linkedin_password)
        driver.find_element_by_xpath('//*[@type="submit"]').click()
        time.sleep(10)
        driver.get("https://www.linkedin.com/feed/hashtag/" + tagName + "/")
        for i in range(1,10000):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(i)
            time.sleep(4)
    except:
        pass

tagName = "javadeveloper" # "devopsjobs" "germanyjobs" "visasponsorship" 
# "" "humanresources" "techjobs" "jobopening" "recruiting" "hiring" 
# #"softwaredesign" "programing" "softwareengineering" 

#FEjobs #freshers2021 #frontenddevelopers #javaprogramming 
# #frontendengineer #javascript #freshersvacancy #freshersworld #freshers 
# #freshgraduates #immediatejoiners #technologyleaders #technologies #developers
#  #careerpath #careergrowth #collegestudents #placementcell #javaarchitect #htmlcss 
# #reactjs #nodejs #frontendjobs

scrollit(tagName=tagName, options=options) 

#jobchange #jobhunt #mljobs  #netherlandsjobs #sydneyjobs #australiajobs #canadajobs #germanyjobs #hungary #norway #oslo
#amsterdamjobs #ukjobs #singaporejobs #malaysiajobs #londonjobs #torontojobs #sweden



        