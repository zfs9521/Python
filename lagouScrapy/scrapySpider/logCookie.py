from selenium import webdriver
import time
from scrapy import Selector
def loginCookie():
    driver=webdriver.Chrome()
    driver.get("https://passport.lagou.com/login/login.html")
    time.sleep(5)
    driver.find_element_by_css_selector('div[data-propertyname="username"] input').send_keys('17864309751')
    driver.find_element_by_css_selector('div[data-propertyname="password"] input').send_keys('xxxxxxx')
    driver.find_element_by_css_selector('div[data-propertyname="submit"] input').click()
    time.sleep(3)
    cookieDict={}
    Cookies=driver.get_cookies()
    print(Cookies)
    for cookie in Cookies:
        cookieDict[cookie['name']]=cookie['value']

    return cookieDict
