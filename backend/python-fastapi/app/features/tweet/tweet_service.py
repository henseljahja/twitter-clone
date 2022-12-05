from fastapi import HTTPException
from starlette import status

from app.features.tweet.tweet_repository import TweetRepository
from app.features.tweet.tweet_schema import (
    TweetRequest,
    TweetResponse,
    TweetResponseWithReplies,
    TweetStatisticsResponse,
)
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import UserAccountResponse


class TweetService:
    def __init__(self):
        self.tweet_repository = TweetRepository()
        self.user_account_repository = UserAccountRepository()

    def get_tweet_statistics_by_tweet_id(
        self, tweet_id: int
    ) -> TweetStatisticsResponse:
        like_number = self.tweet_repository.get_count_like_by_tweet_id(
            tweet_id=tweet_id
        )
        retweet_number = self.tweet_repository.get_count_retweet_by_tweet_id(
            tweet_id=tweet_id
        )
        quote_retweet_number = (
            self.tweet_repository.get_count_quote_retweet_by_tweet_id(tweet_id=tweet_id)
        )
        reply_number = self.tweet_repository.get_count_reply_by_tweet_id(
            tweet_id=tweet_id
        )

        return TweetStatisticsResponse(
            like_number=like_number,
            retweet_number=retweet_number + quote_retweet_number,
            reply_number=reply_number,
        )

    def get_tweets_by_username(self, username: str) -> list[TweetResponse]:
        tweets = self.tweet_repository.get_by_username(username=username)
        tweets_response = [TweetResponse.from_orm(tweet) for tweet in tweets]
        for tweet_response in tweets_response:
            tweet_response.tweet_statistics = self.get_tweet_statistics_by_tweet_id(
                tweet_id=tweet_response.tweet_id
            )
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
    ) -> TweetResponse:
        tweet = self.tweet_repository.create_tweet(
            user_account_id=user_account.user_account_id,
            text=tweet_request.text,
        )
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

    def get_tweet_by_tweet_id(self, tweet_id: int) -> TweetResponseWithReplies:
        tweet = self.tweet_repository.get_tweet_by_id(tweet_id=tweet_id)
        tweet_replies = self.tweet_repository.get_replies(tweet_id=tweet_id)
        tweet_response = TweetResponseWithReplies.from_orm(tweet)
        tweet_response.replies = tweet_replies
        quote_retweet = self.tweet_repository.get_quote_retweet_by_quote_retweet_id(
            quote_retweet_id=tweet_id
        )
        if quote_retweet:
            tweet_response.quote_retweet = TweetResponse.from_orm(quote_retweet)
        return tweet_response
