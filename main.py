from dotenv import load_dotenv
import typer
from apis.instagram import InstagramAPI
from apis.twitter import TwitterAPI
import os


def main(
    username: str,
    twitter_username_override: str = None,
    instagram_username_override: str = None,
):
    load_dotenv()
    twitter_api = TwitterAPI(os.getenv("TWITTER_BEARER_TOKEN"))
    instagram_api = InstagramAPI()

    twitter_username = twitter_username_override or username
    instagram_username = instagram_username_override or username

    twitter_data = twitter_api.get_normalized_user_data(twitter_username)
    instagram_data = instagram_api.get_normalized_user_data(instagram_username)


if __name__ == "__main__":
    typer.run(main)
