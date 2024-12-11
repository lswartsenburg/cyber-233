import os
import requests
from dotenv import load_dotenv
from lib.cache_return_to_file import file_cache


@file_cache()
def fetch_user_details(access_token, base_url, user_agent, username):
    url = f"{base_url}/user/{username}/about"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": user_agent,
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user details: {e}")
        return None


class RedditAPI:
    BASE_URL = "https://oauth.reddit.com"

    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.access_token = self.get_access_token()

    def get_access_token(self):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=auth,
                data=data,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            return None

    def fetch_user_details(self, username):
        if not self.access_token:
            print("Access token is missing. Unable to fetch user details.")
            return None

        return fetch_user_details(
            self.access_token, self.BASE_URL, self.user_agent, username
        )

    def normalize_reddit_data(self, user_data):
        if not user_data:
            return None

        return {
            "username": user_data.get("name"),
            "user_id": user_data.get("id"),
            "account_created": user_data.get("created_utc"),
            "is_employee": user_data.get("is_employee"),
            "is_moderator": user_data.get("is_mod"),
        }

    def get_normalized_user_data(self, username):
        user_data = self.fetch_user_details(username)
        if user_data:
            return self.normalize_reddit_data(user_data)
        else:
            print(f"Failed to fetch or normalize data for username: {username}")
            return None


def main():
    load_dotenv()
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    USER_AGENT = "cyber233 (by u/SnooDucks8255)"

    reddit_api = RedditAPI(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    username = "SnooDucks8255"
    normalized_data = reddit_api.get_normalized_user_data(username)
    if normalized_data:
        print("Normalized Reddit User Data:")
        print(normalized_data)
    else:
        print("User not found or failed to normalize data.")


if __name__ == "__main__":
    main()
