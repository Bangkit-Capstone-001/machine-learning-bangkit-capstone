Updates to keyboard shortcuts … On Thursday, August 1, 2024, Drive keyboard shortcuts will be updated to give you first-letters navigation.Learn more
import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel("data/Gym Exercises Dataset.xlsx")

def get_exercise_details(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract short description
        short_description = soup.find(class_='ExDetail-shortDescription grid-10')
        short_description_text = short_description.get_text(strip=True) if short_description else None

        # Extract instructions
        instructions = None
        section = soup.find('section', class_='ExDetail-section ExDetail-guide')
        if section:
            ol = section.find('ol')
            if ol:
                instructions = '\n'.join([li.get_text(strip=True) for li in ol.find_all('li')])

        # Extract photos
        photos_section = soup.find('section', class_='ExDetail-section ExDetail-photos paywall__xdb-details')
        photos = photos_section.find_all('img', class_='ExImg ExDetail-img js-ex-enlarge') if photos_section else []
        photo_urls = [photo['src'] for photo in photos]

        # Extract guide image
        guide_image_section = soup.find('section', class_='ExDetail-section ExDetail-guide')
        guide_image = guide_image_section.find('img', class_='ExImg') if guide_image_section else None
        guide_image_url = guide_image['src'] if guide_image else None

        return short_description_text, instructions, photo_urls, guide_image_url
    return None, None, [], None

results = []
for idx, row in df.iterrows():
    description_url = row["Description_URL"]
    short_description, instructions, photo_urls, guide_image_url = get_exercise_details(description_url)
    results.append((row["Exercise_Name"], description_url, short_description, instructions, photo_urls, guide_image_url))
    print(row["Exercise_Name"], description_url, short_description, instructions, photo_urls, guide_image_url)

results_df = pd.DataFrame(results, columns=['exercise_name', 'description_url', 'short_description', 'instructions', 'photo_urls', 'guide_image_url'])
results_df.to_csv("data/Gym_Exercises_Bodybuilding.csv", index=False, sep=';')
print("Exercise details and images have been successfully scraped and saved!")