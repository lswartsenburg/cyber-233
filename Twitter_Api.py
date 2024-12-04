import tweepy
import json

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACm7xAEAAAAAjqco7XgA%2FLtcbYAcljHF2fMT7sI%3DuQiDiYdyTMNyR8RSXmKE0a2Tx4tYlVIyyEFTbQrfLRaUmqp7Ml"

def init_client():
    """Initialize the Twitter API client."""
    return tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_user_info(client, username):
    """Fetch detailed user information from Twitter."""
    try:
        user = client.get_user(
            username=username,
            user_fields=["id", "name", "username", "location", "description", "public_metrics"]
        )
        if user.data:
            return {
                "id": user.data.id,
                "name": user.data.name,
                "username": user.data.username,
                "location": user.data.location,
                "description": user.data.description,
                "followers_count": user.data.public_metrics["followers_count"],
                "following_count": user.data.public_metrics["following_count"],
                "tweet_count": user.data.public_metrics["tweet_count"],
            }
        else:
            print(f"User '{username}' not found.")
            return None
    except tweepy.TweepyException as e:
        print(f"Error fetching user info: {e}")
        return None

def fetch_recent_tweets(client, user_id, max_results=5):
    """Fetch recent tweets of a user by user ID."""
    try:
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["id", "text", "created_at"]
        )
        if tweets.data:
            return [
                {"id": tweet.id, "text": tweet.text, "created_at": tweet.created_at}
                for tweet in tweets.data
            ]
        else:
            print(f"No tweets found for user ID '{user_id}'.")
            return []
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return []

def normalize_twitter_data(user_info):
    """
    Normalize Twitter user data into a common format.
    Args:
        user_info (dict): Raw user information fetched from Twitter.
    Returns:
        dict: Normalized user data.
    """
    if not user_info:
        return None

    return {
        "id": user_info.get("id"),
        "name": user_info.get("name"),
        "username": user_info.get("username"),
        "location": user_info.get("location"),
        "bio": user_info.get("description"),
        "profile_picture": None,  # Placeholder as profile picture URL is not fetched here
        "email": None,            # Email is not exposed by the Twitter API
        "connections": user_info.get("followers_count")
    }

def get_normalized_user_data(username):
    """
    Fetch user data by username and return it in a normalized format.
    Args:
        username (str): The Twitter username.
    Returns:
        dict: Normalized user data, or None if the user is not found.
    """
    client = init_client()
    user_info = fetch_user_info(client, username)

    if user_info:
        normalized_data = normalize_twitter_data(user_info)
        return normalized_data
    else:
        print(f"Failed to fetch or normalize data for username: {username}")
        return None

def fetch_twitter_name(client, username):
    """
    Fetch the full name of a user from Twitter using their username.
    Args:
        client (tweepy.Client): Authenticated Twitter API client.
        username (str): The Twitter username.
    Returns:
        dict: A dictionary with firstName and lastName, or None if not found.
    """
    try:
        user_info = fetch_user_info(client, username)
        if user_info and user_info.get("name"):
            full_name = user_info["name"]
            # Split full name into first and last name
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            return {"firstName": first_name, "lastName": last_name}
        return None
    except Exception as e:
        print(f"Error fetching name from Twitter: {e}")
        return None


def save_to_json(filename, data):
    """Save data to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")


def main():
    client = init_client()
    username = "pge444"
    user_info = fetch_user_info(client, username)
    if user_info:
        print(f"User Info: {user_info}")
        tweets = fetch_recent_tweets(client, user_info["id"])
        if tweets:
            print(f"Recent Tweets: {tweets}")
        result = {
            "user_info": user_info,
            "recent_tweets": tweets,
        }
        save_to_json(f"{username}_twitter_data.json", result)

if __name__ == "__main__":
    main()
