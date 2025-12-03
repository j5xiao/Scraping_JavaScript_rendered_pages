import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format="%(message)s")

base_url = 'https://books.toscrape.com/catalogue/page-{page}.html'
detail_url = 'https://books.toscrape.com/catalogue/{title}'

time_out = 10
total_page = 1

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
    url = base_url.format(page=page)
    scrape_page(url, EC.visibility_of_all_elements_located,
                (By.CSS_SELECTOR, '.page_inner'))
    
def parse_index():
    ### on this part, for each line, you only need one tag or class, not both
    elements = browser.find_elements(By.CSS_SELECTOR, 'article .image_container a')
    urls = [el.get_attribute('href') for el in elements]
    return urls

def scrape_detail(url):
    scrape_page(url, EC.visibility_of_element_located,
                (By.TAG_NAME, 'h2'))


def parse_detail():
    name = browser.find_element(By.TAG_NAME, 'h1').text
    price = browser.find_element(By.CSS_SELECTOR, '.price_color').text
    star_p = browser.find_element(By.CSS_SELECTOR, ".star-rating")
    classes = star_p.get_attribute("class")
    star_value = classes.replace("star-rating", "").strip()
    product_description = browser.find_elements(By.CSS_SELECTOR, 'article p')[3].text
    star_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
        }
    star_values = star_map.get(star_value, 0)
    return {
        'Name': name,
        'Score': star_values,
        'Price': price,
        'Product Description': product_description
    }

def main():
    try:
        for page in range(1, total_page + 1):
            scrape_index(1)
            detail_urls = parse_index()

            for detail_url in detail_urls:
                logging.info(f"get detail url {detail_url}")
                scrape_detail(detail_url)
                detail_data = parse_detail()
                logging.info(f"detail data: {detail_data}")
    finally:
        browser.quit()

main()

