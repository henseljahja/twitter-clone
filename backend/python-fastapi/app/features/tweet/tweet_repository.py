from datetime import datetime

from sqlalchemy import and_

from app.features.db.database import db
from app.features.like.like_association import Like
from app.features.retweet.retweet_association import Retweet
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_repository import UserAccountRepository


class TweetRepository:
    def __init__(self):
        self.user_account_repository = UserAccountRepository()

    def get_by_username(self, username: str) -> list[Tweet]:
        tweets = (
            db.session.query(Tweet)
            .join(UserAccount, Tweet.user_account)
            .filter(UserAccount.username == username)
            .all()
        )

        return tweets

    def get_retweets_by_username(self, username: str) -> list[Tweet]:
        user_account = self.user_account_repository.get_by_username(username=username)
        tweets = (
            db.session.query(Tweet)
            .join(Retweet, and_(Tweet.tweet_id == Retweet.c.tweet_id))
            .filter(Retweet.c.user_account_id == user_account.user_account_id)
            .all()
        )

        return tweets

    def get_likes_by_username(self, username: str) -> list[Tweet]:
        user_account = (
            db.session.query(UserAccount)
            .filter(UserAccount.username == username)
            .first()
        )

        tweets = (
            db.session.query(Tweet)
            .join(Like, and_(Tweet.tweet_id == Like.c.tweet_id))
            .filter(Like.c.user_account_id == user_account.user_account_id)
            .all()
        )
        return tweets

    def get_tweet_by_id(self, tweet_id: int) -> Tweet:

        tweet = db.session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
        return tweet

    def create_tweet(self, user_account_id: int, text: str) -> Tweet:
        tweet = Tweet()
        tweet.text = text
        tweet.source = "Twitter for iPhone"
        tweet.created_date = datetime.now()
        tweet.user_account_id = user_account_id

        db.session.add(tweet)
        db.session.commit()
        db.session.refresh(tweet)
        return tweet

    def delete_tweet_by_id(self, tweet_id: int) -> None:
        tweet = db.session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
        db.session.delete(tweet)
        db.session.commit()
        return None
