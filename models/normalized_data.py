from typing import TypedDict


class NormalizedData(TypedDict):
    id: str
    name: str
    username: str
    location: str
    bio: str
    profile_picture: None  # Placeholder as profile picture URL is not fetched here
    email: str
    followers_count: int
    following_count: int
    post_count: int
