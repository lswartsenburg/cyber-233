import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from lib.cache_return_to_file import file_cache


# Configure headless browser options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


def parse_followers(follower_string):
    try:

        # Use regex to extract the number and unit (K, M, etc.)
        match = re.match(r"([\d.]+)([KM]?)\s+followers", follower_string)

        if match:
            value, unit = match.groups()
            value = float(value)  # Convert the value to a float

            # Adjust the value based on the unit
            if unit == "K":
                value *= 1000
            elif unit == "M":
                value *= 1_000_000

            return int(value)  # Return as an integer
    except Exception:
        print(
            f'An error occurred while parsing the follower count from "{follower_string}"'
        )
        return None


def fetch_data_from_selector(driver, selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@file_cache()
def fetch_linkedin_profile_data(username, sleep_time, selectors):
    profile_url = f"https://www.linkedin.com/in/{username}"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(profile_url)
    time.sleep(sleep_time)
    data = {}
    try:
        for key, selector in selectors.items():
            data[key] = fetch_data_from_selector(driver, selector)

        data["followers"] = parse_followers(data["followers"])

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()


class LinkedInScraper:

    selectors = {
        "name": "h1.top-card-layout__title",
        "bio": "section.summary .core-section-container__content",
        "followers": "div.profile-info-subheader > div:nth-child(3) > span:first-child",
        "connections": "div.profile-info-subheader > div:nth-child(3) > span:nth-child(2)",
        "address": "div.profile-info-subheader > div:nth-child(1)",
    }

    sleep_time = 5

    def __init__(self):
        pass

    def get_normalized_user_data(self, username):
        data = fetch_linkedin_profile_data(username, self.sleep_time, self.selectors)
        data["username"] = username
        return data


if __name__ == "__main__":
    scraper = LinkedInScraper()
    data = scraper.get_normalized_user_data("jeremyclarksonamazon")
    print(data)
