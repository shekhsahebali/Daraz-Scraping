import os
import time
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Config
CATEGORIES = {'shoes', 'phone'}
IMAGE_RESIZE = False
TOTAL_PAGES = False
number_of_pages = 1  # 1 page = 40 images
ONLY_NUMBER_IMAGE = 5  # False or N number of images per category



# Initialize Selenium
options = Options()
options.binary_location = "chromium/chrome"
options.add_argument("--window-size=1020,780")
options.add_argument("--disable-gpu")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service("chromiumdriver/chromedriver"), options=options)
for category in CATEGORIES:
    base_url = f"https://www.daraz.com.np/catalog/?q={category}"
    save_dir = f"dataset/{category}"
    os.makedirs(save_dir, exist_ok=True)

    driver.get(base_url)
    print('Initialize on:', base_url)
    time.sleep(3)

    if TOTAL_PAGES:
        try:
            total_pages_element = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[8]/a'
            )
            number_of_pages = int(total_pages_element.text)
        except Exception:
            number_of_pages = 1
    print(f"Total pages: {number_of_pages}")

    total_downloaded = 0 

    for page in range(1, number_of_pages + 1):
        if ONLY_NUMBER_IMAGE and total_downloaded >= ONLY_NUMBER_IMAGE:
            break

        print(f"Scraping page {page}...")
        driver.get(f"{base_url}&page={page}")
        time.sleep(3)

        for i in range(1, 10):
            driver.execute_script(f"window.scrollTo(0, {i*900});")
            time.sleep(1)

        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="general-products"] > div')

        for idx, product in enumerate(products):
            if ONLY_NUMBER_IMAGE and total_downloaded >= ONLY_NUMBER_IMAGE:
                break

            try:
                img = product.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                if src and "jpg" in src:
                    src_url = src.replace("_200x200", "_720x720")
                    url = src_url.rsplit(".jpg", 1)[0] + ".jpg"

                    try:
                        img_data = requests.get(url, timeout=10).content
                        save_path = os.path.join(save_dir, f"{idx}{page}.jpg")
                        with open(save_path, "wb") as f:
                            f.write(img_data)

                        img_pil = Image.open(save_path).convert("RGB")
                        if IMAGE_RESIZE:
                            img_pil = img_pil.resize((224, 224))
                        img_pil.save(save_path)

                        total_downloaded += 1

                    except Exception as e:
                        print(f"Failed to download image {url}: {e}")

            except Exception as e:
                print(f"Failed to process product {idx} on page {page}: {e}")

driver.quit()
print("Scraping completed.")
