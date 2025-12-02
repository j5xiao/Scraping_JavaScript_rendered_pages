import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin

# Enable logging output
logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE_URL = "https://spa2.scrape.center/"
INDEX_URL = "https://spa2.scrape.center/page/{page}"
time_out = 10
total_page = 10

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(browser, time_out)


def scrape_page(url, conditions, locator):
    logging.info(f"scraping {url}")
    try:
        browser.get(url)
        wait.until(conditions(locator))
    except TimeoutException:
        logging.error(f"error while scraping {url}", exc_info=True)


def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_page(url, EC.visibility_of_all_elements_located,
                (By.CSS_SELECTOR, '.item'))


def parse_index():
    elements = browser.find_elements(By.CSS_SELECTOR, '#index .item .name')
    urls = [el.get_attribute('href') for el in elements]
    return urls


def scrape_detail(url):
    scrape_page(url, EC.visibility_of_element_located,
                (By.TAG_NAME, 'h2'))


def parse_detail():
    name = browser.find_element(By.TAG_NAME, 'h2').text
    categories = [el.text for el in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
    score = browser.find_element(By.CLASS_NAME, 'score').text
    return name, categories, score


def main():
    try:
        for page in range(1, total_page + 1):
            scrape_index(page)
            detail_urls = parse_index()

            for detail_url in detail_urls:
                logging.info(f"get detail url {detail_url}")
                scrape_detail(detail_url)
                detail_data = parse_detail()
                logging.info(f"detail data: {detail_data}")
    finally:
        browser.quit()


main()
