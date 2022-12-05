from __future__ import annotations

from datetime import datetime
from typing import List, Union

from app.common.base.base_schema import BaseSchema


class UserAccountStatisticsResponse(BaseSchema):
    follower_count: int | None
    following_count: int | None


class UserAccountResponse(BaseSchema):
    user_account_id: int | None
    name: str | None
    username: str | None
    about: str | None
    categories: str | None
    location: str | None
    website: str | None
    joined_date: datetime | None
    birth_date: datetime | None
    is_verified: bool | None
    is_private: bool | None
    is_official_account: bool | None
    email: str | None
    password: str | None
    phone_number: str | None
    country: str | None
    profile_picture: str | None
    user_account_statistics: UserAccountStatisticsResponse | None
    tweets: Union["List[TweetResponse]", None]

    class Config:
        orm_mode = True


from app.features.tweet.tweet_schema import TweetResponse

UserAccountResponse.update_forward_refs()


class UserAccountSignUpRequest(BaseSchema):
    email: str | None
    password: str | None
    username: str | None
