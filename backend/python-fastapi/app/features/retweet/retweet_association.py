from sqlalchemy import Column, ForeignKey, Table

from app.common.base.base_config import BaseTableObject

Retweet = Table(
    "retweet",
    BaseTableObject.metadata,
    Column("user_account_id", ForeignKey("user_account.user_account_id")),
    Column("tweet_id", ForeignKey("tweet.tweet_id")),
)
