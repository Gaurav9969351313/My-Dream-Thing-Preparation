from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import parameters, csv, os.path, time

def search_and_view_profile(keywords, till_page, writer):
    for page in range(1, till_page + 1):

        print('\nINFO: Checking on page %s' % (page))
        query_url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B"101282230"%5D&keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
        driver.get(query_url)
        time.sleep(2)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(2)
        # linkedin_urls = driver.find_elements_by_class_name('reusable-search__result-container')
        profile_urls = driver.find_elements_by_class_name('entity-result__title-text--black')
        print('INFO: %s Profiles found on page %s' % (len(profile_urls), page))
        for index, result in enumerate(profile_urls, start=1):
            text = result.text.split('\n')[0]
            aTag = result.find_element_by_css_selector('.entity-result__title-text--black a, .entity-result__title-text--black a:visited')
            link = aTag.get_attribute('href')
            print(link)
            arr = link.split('/')
            temp = arr[4]
            profileName = temp.split('?')[0]
            print(profileName)
            detailsPage ='https://www.linkedin.com/in/' + profileName + '/detail/contact-info/'
            print('================')
            writer.writerow([link, profileName, detailsPage])
            driver.execute_script('window.open("'+ link +'","_blank");')
            # time.sleep(2)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com/login')
driver.find_element_by_id('username').send_keys(parameters.linkedin_username)
driver.find_element_by_id('password').send_keys(parameters.linkedin_password)
driver.find_element_by_xpath('//*[@type="submit"]').click()
time.sleep(10)

file_name = parameters.profile_viewed_file
file_exists =  os.path.isfile(file_name)
writer = csv.writer(open(file_name, 'a'))
if not file_exists: writer.writerow(['url','username', 'detailsPageLink'])


search_and_view_profile(keywords=parameters.keywords, till_page=parameters.till_page, writer=writer)

# Close browser
# driver.quit()


# https://www.linkedin.com/in/katarzynameister/?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABL2hLgB5ofjlN8Azr8VAJfBG3VwRs5_N_A

