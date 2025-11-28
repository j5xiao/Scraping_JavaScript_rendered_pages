from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

browser = webdriver.Chrome()
url = "https://ssr1.scrape.center/"
try:
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    print(browser.current_url)
    # print(browser.page_source)
    print([i.text for i in browser.find_elements(By.CSS_SELECTOR, '.name')])
finally:
    browser.close()