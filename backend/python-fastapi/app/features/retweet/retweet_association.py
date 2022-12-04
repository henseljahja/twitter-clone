from sqlalchemy import Column, ForeignKey, Table

from app.features.db.db_session import BaseTableObject

Retweet = Table(
    "retweet",
    BaseTableObject.metadata,
    Column("user_account_id", ForeignKey("user_account.user_account_id")),
    Column("tweet_id", ForeignKey("tweet.tweet_id")),
)
