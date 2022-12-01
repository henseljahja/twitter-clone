from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.util import db_util
from app.features.tweet.tweet_schema import TweetResponse
from app.features.tweet.tweet_service import TweetService
from app.features.user_account.user_account_schema import UserAccountResponse
from app.features.user_account.user_account_service import UserAccountService

tweet_service = TweetService()
tweet_controller = APIRouter()


@tweet_controller.get(
    "/username/{username}/tweet",
    response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_by_username(
    *, session: Session = Depends(db_util.get_session), username: str
) -> list[TweetResponse]:
    return tweet_service.get_by_username(session=session, username=username)


@tweet_controller.get(
    "/username/{username}/retweets",
    response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_retweet_by_username(
    *, session: Session = Depends(db_util.get_session), username: str
) -> list[TweetResponse]:
    return tweet_service.get_retweets_by_username(session=session, username=username)


@tweet_controller.get(
    "/username/{username}/likes",
    response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_retweet_by_username(
    *, session: Session = Depends(db_util.get_session), username: str
) -> list[TweetResponse]:
    return tweet_service.get_likes_by_username(session=session, username=username)
