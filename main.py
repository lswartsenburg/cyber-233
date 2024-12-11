from dotenv import load_dotenv
import typer
from apis.instagram import InstagramAPI
from apis.reddit import RedditAPI
from apis.twitter import TwitterAPI
from pprint import pprint
import os

from apis.youtube import YouTubeAPI
from privacy_score import calculate_overall_privacy_score
from scrapers.linkedin import LinkedInScraper


def main(
    username: str,
    twitter_username_override: str = None,
    instagram_username_override: str = None,
    youtube_username_override: str = None,
    linkedin_username_override: str = None,
    reddit_username_override: str = None,
):
    load_dotenv()

    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = "cyber233 (by u/SnooDucks8255)"

    twitter_api = TwitterAPI(os.getenv("TWITTER_BEARER_TOKEN"))
    instagram_api = InstagramAPI()
    youtube_api = YouTubeAPI(os.getenv("YOUTUBE_API_KEY"))
    reddit_api = RedditAPI(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    linkedin_scraper = LinkedInScraper()

    twitter_username = twitter_username_override or username
    instagram_username = instagram_username_override or username
    linkedin_username = linkedin_username_override or username  # "jeremyclarksonamazon"
    youtube_username = youtube_username_override or username
    reddit_username = reddit_username_override or username

    try:
        twitter_data = twitter_api.get_normalized_user_data(twitter_username)
        print(f"Fetched Twitter data for {twitter_username}")
    except Exception as e:
        print(f"An error occurred while fetching Twitter data: {e}")
        twitter_data = None

    try:
        instagram_data = instagram_api.get_normalized_user_data(instagram_username)
        print(f"Fetched Instagram data for {instagram_username}")
    except Exception as e:
        print(f"An error occurred while fetching Instagram data: {e}")
        instagram_data = None

    try:
        linkedin_data = linkedin_scraper.get_normalized_user_data(linkedin_username)
        print(f"Fetched LinkedIn data for {linkedin_username}")
    except Exception as e:
        print(f"An error occurred while fetching LinkedIn data: {e}")
        linkedin_data = None

    try:
        youtube_data = youtube_api.get_normalized_channel_data(youtube_username)
        print(f"Fetched YouTube data for {youtube_username}")
    except Exception as e:
        print(f"An error occurred while fetching YouTube data: {e}")
        youtube_data = None

    try:
        reddit_data = reddit_api.get_normalized_user_data(reddit_username)
        print(f"Fetched Reddit data for {reddit_username}")
    except Exception as e:
        print(f"An error occurred while fetching Reddit data: {e}")
        reddit_data = None

    print(f"Data for {username}:")
    all_data = {
        "twitter": twitter_data,
        "instagram": instagram_data,
        "linkedin": linkedin_data,
        "youtube": youtube_data,
        "reddit": reddit_data,
    }
    pprint(all_data)

    privacy_score = calculate_overall_privacy_score(all_data)

    print(f"\n\n\n\n####### Privacy score #######")
    print(privacy_score)


if __name__ == "__main__":
    typer.run(main)
