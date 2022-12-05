from __future__ import annotations

from datetime import datetime

from sqlalchemy import and_, func

from app.features.db.database import db
from app.features.like.like_association import Like
from app.features.retweet.retweet_association import Retweet
from app.features.tweet.quote_retweet.quote_retweet_association import QuoteRetweet
from app.features.tweet.reply.reply_association import Reply
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_repository import UserAccountRepository


class TweetRepository:
    def __init__(self):
        self.user_account_repository = UserAccountRepository()

    def get_count_like_by_tweet_id(self, tweet_id: int) -> int:
        like_number = (
            db.session.query(func.count(Reply.c.tweet_id))
            .filter(Reply.c.tweet_id == tweet_id)
            .scalar()
        )
        return like_number

    def get_count_retweet_by_tweet_id(self, tweet_id: int) -> int:
        retweet_number = (
            db.session.query(func.count(Retweet.c.tweet_id))
            .filter(Retweet.c.tweet_id == tweet_id)
            .scalar()
        )
        return retweet_number

    def get_count_quote_retweet_by_tweet_id(self, tweet_id: int) -> int:
        quote_retweet_number = (
            db.session.query(func.count(QuoteRetweet.c.tweet_id))
            .filter(QuoteRetweet.c.tweet_id == tweet_id)
            .scalar()
        )
        return quote_retweet_number

    def get_count_reply_by_tweet_id(self, tweet_id: int) -> int:
        reply_number = (
            db.session.query(func.count(Reply.c.tweet_id))
            .filter(Reply.c.tweet_id == tweet_id)
            .scalar()
        )
        return reply_number

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

    def get_replies(self, tweet_id: int) -> list[Tweet]:
        tweet_id_to_search = self.get_tweet_by_id(tweet_id=tweet_id)
        tweets = (
            db.session.query(Tweet)
            .join(Reply, and_(Tweet.tweet_id == Reply.c.reply_id))
            .filter(Reply.c.tweet_id == tweet_id_to_search.tweet_id)
            .all()
        )
        return tweets

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

    def get_quote_retweet_by_quote_retweet_id(
        self, quote_retweet_id: int
    ) -> Tweet | None:

        quote_retweet = (
            db.session.query(Tweet)
            .join(QuoteRetweet, and_(Tweet.tweet_id == QuoteRetweet.c.tweet_id))
            .filter(QuoteRetweet.c.quote_retweet_id == quote_retweet_id)
        ).first()
        return quote_retweet
