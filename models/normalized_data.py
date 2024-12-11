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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "location": self.location,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "email": self.email,
            "followers_count": self.followers_count,
            "following_count": self.following_count,
            "post_count": self.post_count,
        }

    @classmethod
    def from_dict(cls, data):
        return NormalizedData(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            location=data["location"],
            bio=data["bio"],
            profile_picture=data["profile_picture"],
            email=data["email"],
            followers_count=data["followers_count"],
            following_count=data["following_count"],
            post_count=data["post_count"],
        )
