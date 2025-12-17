import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Config
CATEGORIES = {'shoes', 'phone'}
TOTAL_PAGES = False
number_of_pages = 1  # 1 page = 40 url

# Initialize Selenium
options = Options()
options.binary_location = "chromium/chrome"
options.add_argument("--window-size=1020,780")
options.add_argument("--disable-gpu")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service("chromiumdriver/chromedriver"), options=options)
for category in CATEGORIES:
    base_url = f"https://www.daraz.com.np/catalog/?q={category}"


    driver.get(base_url)
    time.sleep(3)


    if TOTAL_PAGES:
        try:
            total_pages_element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a')
            number_of_pages = int(total_pages_element.text)
        except:
            number_of_pages = 1 
    print(f"Total pages detected: {number_of_pages}")

    product_links = []

    # Loop through all pages
    for page in range(1, number_of_pages + 1):
        print(f"Scraping page {page}...")
        driver.get(f"{base_url}&page={page}")
        time.sleep(3)
        

        for i in range(1, 10):
            driver.execute_script(f"window.scrollTo(0, {i*900});")
            time.sleep(1)
        

        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="general-products"] > div')
        for product in products:
            try:
                link = product.find_element(By.TAG_NAME, "a")
                href = link.get_attribute('href')
                if href:
                    product_links.append(href)
            except:
                continue

driver.quit()


with open("product_links.txt", "w") as f:
    for url in product_links:
        f.write(url + "\n")

print(f"Collected {len(product_links)} product links from {number_of_pages} pages")
print("Links saved to product_links.txt")
