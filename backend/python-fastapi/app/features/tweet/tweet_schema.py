from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

from app.common.base.base_schema import BaseSchema


class TweetResponse(BaseSchema):
    tweet_id: int | None
    text: str | None
    source: str | None
    created_date: datetime | None
    user_account_id: int | None
    user_account: Union["UserAccountResponse", None]

    class Config:
        orm_mode = True


from app.features.user_account.user_account_schema import UserAccountResponse

TweetResponse.update_forward_refs()


class TweetRequest(BaseSchema):
    text: str | None
