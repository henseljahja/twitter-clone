from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.common.util.log_util import log
from app.features.tweet.tweet import Tweet
from app.features.tweet.tweet_repository import TweetRepository
from app.features.tweet.tweet_schema import TweetResponse


class TweetService:
    def __init__(self):
        self.tweet_repository = TweetRepository()

    def get_by_username(self, session: Session, username: str) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_by_username(
            session=session, username=username
        )
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response

    def get_retweets_by_username(
        self, session: Session, username: str
    ) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_retweets_by_username(
            session=session, username=username
        )
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response

    def get_likes_by_username(
        self, session: Session, username: str
    ) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_likes_by_username(
            session=session, username=username
        )
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response
