Updates to keyboard shortcuts … On Thursday, August 1, 2024, Drive keyboard shortcuts will be updated to give you first-letters navigation.Learn more
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

df = pd.read_excel("data/Gym Exercises Dataset.xlsx")


def get_youtube_info(query):
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?sp=EgQYATAB&search_query=how+to+do+a+{query}"

    driver.get(url)
    time.sleep(3)
    video = driver.find_element(By.XPATH, '//a[@id="video-title"]')
    thumbnail = video.find_element(
        By.XPATH, '//img[@class="yt-core-image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded"]')
    title = thumbnail.find_element(
        By.XPATH, '//a[@class="yt-simple-endpoint style-scope ytd-video-renderer"]')

    if video and thumbnail and title:
        video_url = video.get_attribute('href')
        thumbnail_url = thumbnail.get_attribute('src')
        video_title = title.get_attribute('title')
        return video_url, thumbnail_url, video_title
    return None, None


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

results = []
for exercise in df["Exercise_Name"]:
    video_url, thumbnail_url, video_title = get_youtube_info(exercise)
    results.append((exercise, video_url, thumbnail_url, video_title))
    print(exercise, video_url, thumbnail_url, video_title)

driver.quit()

results_df = pd.DataFrame(
    results, columns=['exercise_name', 'youtube_url', 'thumbnail_url', 'youtube_title'])
results_df.to_csv(
    "data/Gym_Exercises_YouTube.csv", index=False)
print("YouTube URLs and thumbnails have been successfully scraped and saved!")