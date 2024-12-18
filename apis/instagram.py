import requests
import json
from lib.cache_return_to_file import file_cache
from models.normalized_data import NormalizedData


@file_cache()
def scrape_user(username: str):
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


class InstagramAPI:

    def get_user(self, username: str):
        return scrape_user(username)

    def normalize_instagram_data(self, data: dict) -> NormalizedData:
        """Normalize Instagram user data"""
        name = data.get("full_name")
        username = data.get("username")
        location = data.get("location")  # May be None if not present
        bio = data.get("biography")
        profile_picture = data.get("profile_pic_url")
        email = data.get(
            "business_email"
        )  # This key may not be present if not a business account
        followers_count = data.get("edge_followed_by", {}).get("count")
        following_count = data.get("edge_follow", {}).get("count")
        post_count = data.get("edge_owner_to_timeline_media", {}).get("count")
        normalized_data = NormalizedData(
            name=name,
            username=username,
            location=location,
            bio=bio,
            profile_picture=profile_picture,
            email=email,
            followers_count=followers_count,
            following_count=following_count,
            post_count=post_count,
        )
        return normalized_data

    def get_normalized_user_data(self, username: str) -> NormalizedData:
        data = self.get_user(username)
        normalized_data = self.normalize_instagram_data(data)
        return normalized_data


if __name__ == "__main__":
    api = InstagramAPI()
    user_data = api.get_user("jeremyclarkson1")
    print(json.dumps(user_data, indent=4))
