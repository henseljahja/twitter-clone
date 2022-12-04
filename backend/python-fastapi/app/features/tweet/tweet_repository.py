from datetime import datetime

from sqlalchemy import and_, select

from app.features.db.database import db
from app.features.db.db_session import session
from app.features.db.transactional import Transactional
from app.features.like.like_association import Like
from app.features.retweet.retweet_association import Retweet
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount


class TweetRepository:
    def get_by_username(self, username: str) -> list[Tweet]:
        tweets = (
            db.session.query(Tweet)
            .join(UserAccount, Tweet.user_account)
            .filter(UserAccount.username == username)
            .all()
        )

        return tweets

    async def get_retweets_by_username(self, username: str) -> list[Tweet]:
        user_account = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )
        tweets = (
            (
                await (
                    session.execute(
                        select(Tweet)
                        .join(Retweet, and_(Tweet.tweet_id == Retweet.c.tweet_id))
                        .filter(
                            Retweet.c.user_account_id == user_account.user_account_id
                        )
                    )
                )
            )
            .scalars()
            .all()
        )

        return tweets

    async def get_likes_by_username(self, username: str) -> list[Tweet]:
        user_account = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )

        tweets = (
            (
                await (
                    session.execute(
                        select(Tweet)
                        .join(Like, and_(Tweet.tweet_id == Like.c.tweet_id))
                        .filter(Like.c.user_account_id == user_account.user_account_id)
                    )
                )
            )
            .scalars()
            .all()
        )
        return tweets

    async def get_tweet_by_id(self, tweet_id: int) -> Tweet:

        tweet = (
            (await (session.execute(select(Tweet).filter(Tweet.tweet_id == tweet_id))))
            .scalars()
            .first()
        )
        return tweet

    # @Transactional(propagation=Propagation.REQUIRED)
    async def create_tweet(self, user_account_id: int, text: str) -> Tweet:
        tweet = Tweet()
        tweet.text = text
        tweet.source = "Twitter for iPhone"
        tweet.created_date = datetime.now()
        tweet.user_account_id = user_account_id

        session.add(tweet)
        await session.commit()
        await session.flush()
        return tweet

    @Transactional()
    async def delete_tweet_by_id(self, tweet_id: int) -> None:
        tweet = (
            (await (session.execute(select(Tweet).filter(Tweet.tweet_id == tweet_id))))
            .scalars()
            .first()
        )
        await session.delete(tweet)
        return None
