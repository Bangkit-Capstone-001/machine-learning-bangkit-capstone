Updates to keyboard shortcuts … On Thursday, August 1, 2024, Drive keyboard shortcuts will be updated to give you first-letters navigation.Learn more
import os
import requests
import base64
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

df = pd.read_excel("data/Food 101 prep.xlsx")


def get_google_images(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?udm=2&q={query}"

    driver.get(url)
    driver.maximize_window()
    driver.execute_script("window.scrollBy(0, 4000)")
    time.sleep(10)
    images = driver.find_elements(By.XPATH, '//img[@class="YQ4gaf"]')
    idx = 0

    for _, image in enumerate(images):
        image_src = image.get_attribute('src')
        if image_src.startswith('data:image/jpeg'):
            print(os.path.getsize(f"images/{query}_{idx+1}.jpg"))
            if os.path.getsize(f"images/{query}_{idx+1}.jpg") == 0:
                header, base64_data = image_src.split(',', 1)
                image_data = base64.b64decode(base64_data)
                with open(os.path.join('images', f"{query}_{idx+1}.jpg"), 'wb') as handler:
                    handler.write(image_data)
                idx += 1
                print(f'jpeg Successfully scraped and saved {query}_{idx+1}.jpg')
        elif image_src.startswith('https://'):
            print(os.path.getsize(f"images/{query}_{idx+1}.jpg"))
            if os.path.getsize(f"images/{query}_{idx+1}.jpg") == 0:
                img_data = requests.get(image_src).content
                with open(os.path.join('images', f"{query}_{idx+1}.jpg"), 'wb') as handler:
                    handler.write(img_data)
                idx += 1
                print(f'https Successfully scraped and saved {query}_{idx+1}.jpg')


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

for food_name in df["Tambahan (Web Scraping)"]:
    get_google_images(food_name.strip())

driver.quit()