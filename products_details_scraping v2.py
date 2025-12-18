import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ---------------- CONFIG ----------------
CATEGORIES = {'fashion'}
TOTAL_PAGES = False
ONLY_NUMBER_PRODUCTS = 5                # False or N number of product per category
number_of_pages = 1                     # 1 page = 40 product
CSV_FILE = "daraz_products_v2.csv"

# ---------------- SELENIUM SETUP ----------------
options = Options()
options.binary_location = "chromium/chrome"
options.add_argument("--window-size=1020,780")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=Service("chromiumdriver/chromedriver"),
    options=options
)

csv_exists = os.path.exists(CSV_FILE)

# ---------------- SCRAPING ----------------
for category in CATEGORIES:
    base_url = f"https://www.daraz.com.np/{category}/"
    driver.get(base_url)
    time.sleep(3)

    if TOTAL_PAGES:
        try:
            total_pages_element = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-item-8 a")
            number_of_pages = int(total_pages_element.text)
        except:
            number_of_pages = 1

    print(f"[{category}] Pages: {number_of_pages}")

    total_scrap_data = 0

    for page in range(1, number_of_pages + 1):
        if ONLY_NUMBER_PRODUCTS and total_scrap_data >= ONLY_NUMBER_PRODUCTS:
            break

        driver.get(f"{base_url}&page={page}")
        time.sleep(3)

        for i in range(1, 10):
            driver.execute_script(f"window.scrollTo(0, {i*900});")
            time.sleep(0.5)

        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="general-products"] a')

        product_links = list({p.get_attribute("href") for p in products if p.get_attribute("href")})

        for link in product_links:
            if ONLY_NUMBER_PRODUCTS and total_scrap_data >= ONLY_NUMBER_PRODUCTS:
                break

            driver.get(link)
            time.sleep(3)
            
            driver.execute_script(f"window.scrollTo(0, {i*900});")
            time.sleep(1)

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
                image_url = driver.find_element(By.CLASS_NAME, "gallery-preview-panel__content").find_element(By.TAG_NAME, "img").get_attribute("src")

                ratings_text = driver.find_element(By.CLASS_NAME, "pdp-review-summary__link").text
                ratings = int(re.search(r'\d+', ratings_text).group())
                
                try:

                  brand = driver.find_element(By.CLASS_NAME, "pdp-product-brand").find_element(By.TAG_NAME, "a").text
                except:
                  brand = driver.find_element(By.CLASS_NAME, "pdp-product-brand").find_element(By.CLASS_NAME, "pdp-product-brand__brand").text
                    

                price_text = driver.find_element(By.CLASS_NAME, "pdp-product-price").text.replace(",", "")
                price = int(re.search(r'\d+', price_text).group())

                try:
                    color = driver.find_element(By.CLASS_NAME, "sku-name").text
                except:
                    color = ""

                df = pd.DataFrame([{
                    "title": title,
                    "brand": brand,
                    "price": price,
                    "ratings": ratings,
                    "image_url": image_url,
                    "color": color
                }])

                df.to_csv(CSV_FILE,mode="a",index=False,header=not csv_exists)
                csv_exists = True
                total_scrap_data += 1

                print(f"Saved: {title}")

            except Exception as e:
                print(f"Failed product: {e}")

driver.quit()
print("Scraping completed.")
