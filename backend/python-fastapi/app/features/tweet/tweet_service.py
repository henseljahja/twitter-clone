from typing import Any

from fastapi import HTTPException
from starlette import status

from app.common.base.log_config import log
from app.features.tweet.tweet_repository import TweetRepository
from app.features.tweet.tweet_schema import TweetRequest, TweetResponse
from app.features.user_account.follower.follower_repository import FollowerRepository
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import UserAccountResponse


class TweetService:
    def __init__(self):
        self.tweet_repository = TweetRepository()
        self.user_account_repository = UserAccountRepository()
        self.follower_repository = FollowerRepository()

    def get_tweets_by_username(self, username: str) -> Any:

        tweets = self.tweet_repository.get_by_username(username=username)
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response

    def get_retweets_by_username(self, username: str) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_retweets_by_username(username=username)
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response

    def get_likes_by_username(self, username: str) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_likes_by_username(username=username)
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        return tweets_response

    def create_tweet(
        self,
        user_account: UserAccountResponse,
        tweet_request: TweetRequest,
    ):
        tweet = self.tweet_repository.create_tweet(
            user_account_id=user_account.user_account_id,
            text=tweet_request.text,
        )
        log.debug(f"create_tweet @ Service => tweet {tweet.__dict__}")
        tweet_response = TweetResponse.from_orm(tweet)
        return tweet_response

    def delete_tweet(
        self,
        user_account: UserAccountResponse,
        tweet_id: int,
    ) -> None:
        tweet = self.tweet_repository.get_tweet_by_id(tweet_id=tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="TWEET NOT FOUND"
            )
        if tweet.user_account_id != user_account.user_account_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED USER"
            )
        self.tweet_repository.delete_tweet_by_id(tweet_id=tweet_id)
        return None
