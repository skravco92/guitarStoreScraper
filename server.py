from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Create a Chrome webdriver
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www.gitarcentrum.hu/category/elektro-klasszikus-gitarok"

# Open the URL in the webdriver
driver.get(url)
print(driver.title)

# Create empty lists to store data
models = []
links = []
prices = []
specs = []

# Create a list of URLs to scrape
urls = []
for page_num in range(1, 4):
    urls.append(f"{url}?ppage={page_num}&ipp=12")

# Set initial current_page_index
current_page_index = 0

# Iterate through each URL
while current_page_index < 3:
    driver.get(urls[current_page_index])
    try:
        # Wait for the products element to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "products")))
        # Find all items on the page
        items = products.find_elements(By.CLASS_NAME, "caption")
        for item in items:
            # Get the model, link, and price for each item
            model = item.find_element(
                By.CSS_SELECTOR, "h2").get_attribute("innerText")
            models.append(model)
            href = item.find_element(
                By.CSS_SELECTOR, "a").get_attribute("href")
            links.append(href)
            price = item.find_element(
                By.CLASS_NAME, "price").get_attribute("innerText")
            prices.append(price)
    except:
        print(None)
    current_page_index += 1
    time.sleep(2)

# Iterate through each link to get the specs
for i in (links):
    print(i)
    driver.get(i)
    try:
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        description = soup.find('div', {'itemprop': 'description'})
        specs.append(description.text.strip())
    except:
        print(None)
    time.sleep(2)


exGuitars = pd.DataFrame({
    'Model': models,
    'Price': prices,
    'Link': links,
    'Specifications': specs
})

exGuitars.to_csv("classElectricGuitars.csv")
