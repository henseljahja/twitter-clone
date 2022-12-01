from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.common.util.log_util import log
from app.features.like.like_association import Like
from app.features.retweet.retweet_association import Retweet
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount


class TweetRepository:
    def get_by_username(self, session: Session, username: str) -> list[Tweet]:
        list_of_tweet = (
            session.query(Tweet)
            .join(UserAccount, Tweet.user_account)
            .filter(UserAccount.username == username)
            .all()
        )

        return list_of_tweet

    def get_retweets_by_username(self, session: Session, username: str) -> list[Tweet]:
        user_account = (
            session.query(UserAccount).filter(UserAccount.username == username).first()
        )
        tweets = (
            session.query(Tweet)
            .join(Retweet, and_(Tweet.tweet_id == Retweet.c.tweet_id))
            .filter(Retweet.c.user_account_id == user_account.user_account_id)
            .all()
        )
        return tweets

    def get_likes_by_username(self, session: Session, username: str) -> list[Tweet]:
        user_account = (
            session.query(UserAccount).filter(UserAccount.username == username).first()
        )
        tweets = (
            session.query(Tweet)
            .join(Like, and_(Tweet.tweet_id == Like.c.tweet_id))
            .filter(Like.c.user_account_id == user_account.user_account_id)
            .all()
        )
        return tweets
