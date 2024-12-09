import os
import requests
import hashlib
import pickle
from dotenv import load_dotenv
from lib.cache_return_to_file import file_cache

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    @file_cache()
    def search_channel_by_username(self, username):
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "q": username,
            "type": "channel",
            "key": self.api_key,
            "maxResults": 1,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            items = response.json().get("items", [])
            if items:
                return items[0]["snippet"]["channelId"]
            else:
                print(f"No channel found for username: {username}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error searching for channel: {e}")
            return None

    @file_cache()
    def fetch_channel_details(self, channel_id):
        url = f"{self.base_url}/channels"
        params = {
            "part": "id,snippet,contentDetails,statistics,status",
            "id": channel_id,
            "key": self.api_key,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("items", [])
            return data[0] if data else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching channel details: {e}")
            return None

    def normalize_youtube_data(self, channel_data):
        if not channel_data:
            return None

        snippet = channel_data.get("snippet", {})
        statistics = channel_data.get("statistics", {})
        status = channel_data.get("status", {})
        content_details = channel_data.get("contentDetails", {})
        return {
            "id": channel_data.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "statistics": {
            "subscriber_count": statistics.get("subscriberCount"),
            "view_count": statistics.get("viewCount"),
            "video_count": statistics.get("videoCount"),
            },
            "contentDetails": content_details,
            "location": snippet.get("country"),
            "privacyStatus": status.get("privacyStatus"),
            "isLinked": status.get("isLinked"),
        }

    def get_normalized_channel_data(self, username):
        channel_id = self.search_channel_by_username(username)
        if channel_id:
            channel_data = self.fetch_channel_details(channel_id)
            if channel_data:
                return self.normalize_youtube_data(channel_data)
        print(f"Failed to fetch or normalize data for username: {username}")
        return None


if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube_api = YouTubeAPI(API_KEY)

    username = "fern"  # Replace with the username to search
    normalized_data = youtube_api.get_normalized_channel_data(username)
    if normalized_data:
        print("Normalized YouTube Channel Data:")
        print(normalized_data)
    else:
        print("Channel not found or failed to normalize data.")
