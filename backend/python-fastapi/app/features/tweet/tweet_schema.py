from __future__ import annotations

from datetime import datetime
from typing import Union

from app.common.base.base_schema import BaseSchema


class TweetStatisticsResponse(BaseSchema):
    like_number: int | None
    retweet_number: int | None
    reply_number: int | None


class TweetResponse(BaseSchema):
    tweet_id: int | None
    text: str | None
    source: str | None
    created_date: datetime | None
    user_account_id: int | None
    tweet_statistics: TweetStatisticsResponse | None
    user_account: Union["UserAccountResponse", None]

    class Config:
        orm_mode = True


from app.features.user_account.user_account_schema import UserAccountResponse

TweetResponse.update_forward_refs()


class TweetRequest(BaseSchema):
    text: str | None


class TweetResponseWithReplies(TweetResponse):
    replies: list[TweetResponse] | None
    quote_retweet: TweetResponse | None
