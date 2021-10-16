from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import parameters, csv, os.path, time


# Functions 
def search_and_send_request(keywords, till_page, writer):
    counter = 0
    for page in range(1, till_page + 1):
        print('\nINFO: Checking on page %s' % (page))
        query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
        driver.get(query_url)
        time.sleep(5)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(5)
        linkedin_urls = driver.find_elements_by_class_name('reusable-search__result-container')
        print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
        for index, result in enumerate(linkedin_urls, start=1):
            text = result.text.split('\n')[0]
            connection_action = result.find_elements_by_class_name('artdeco-button__text')
            if connection_action:
                connection = connection_action[0]
            else: 
                print("%s ) CANT: %s" % (index, text))
                continue
            if connection.text == 'Connect':
                try:
                    coordinates = connection.location_once_scrolled_into_view # returns dict of X, Y coordinates
                    driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                    time.sleep(5)
                    connection.click()
                    if driver.find_elements_by_class_name('artdeco-button--primary')[0].is_enabled():
                       # driver.find_elements_by_class_name('artdeco-button--primary')[0].click()
                       driver.find_elements_by_tag_name('button')[1].click()
                       time.sleep(2)
                       driver.find_element_by_class_name('connect-button-send-invite__custom-message').send_keys(parameters.note)
                       time.sleep(2)
                       driver.find_elements_by_class_name('artdeco-button--primary')[0].click()

                       # artdeco-button--muted
                    print("%s ) CANT: %s" % (index, text))
                except Exception as e:
                    print('%s ) ERROR: %s' % (index, text))
                time.sleep(5)
            elif connection.text == 'Pending':
                    print("%s ) PENDING: %s" % (index, text))
            else:
                    if text : print("%s ) CANT: %s" % (index, text))
                    else: print("%s ) ERROR: You might have reached limit" % (index))



# Login
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com/login')
driver.find_element_by_id('username').send_keys(parameters.linkedin_username)
driver.find_element_by_id('password').send_keys(parameters.linkedin_password)
driver.find_element_by_xpath('//*[@type="submit"]').click()
time.sleep(10)
#name = driver.find_elements_by_class_name('profile-rail-card__actor-link')[0].text.replace(' ', '')

# CSV file loging
#file_name = name + '_' + parameters.file_name.capitalize()
file_name = parameters.file_name
file_exists =  os.path.isfile(file_name)
writer = csv.writer(open(file_name, 'a'))
if not file_exists: writer.writerow(['Connection Summary'])

# Search
search_and_send_request(keywords=parameters.keywords, till_page=parameters.till_page, writer=writer)

# Close browser
driver.quit()