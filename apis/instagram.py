import requests
import json
import httpx
from lib.cache_return_to_file import file_cache


class InstagramAPI:

    @file_cache()
    def scrape_user(self, username: str):
        """Scrape Instagram user's data"""
        headers = {
            "x-ig-app-id": "936619743392459",
            # pylint: disable=line-too-long
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
        }
        result = requests.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            headers=headers,
            timeout=10,
        )
        data = result.json()
        return data["data"]["user"]

    def get_normalized_user_data(self, username: str):
        return self.scrape_user(username)


if __name__ == "__main__":
    api = InstagramAPI()
    user_data = api.scrape_user("jeremyclarkson1")
    print(json.dumps(user_data, indent=4))
