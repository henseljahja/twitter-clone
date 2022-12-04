from sqlalchemy import Column, ForeignKey, Table

from app.features.db.database import BaseModel

Like = Table(
    "like",
    BaseModel.metadata,
    Column("user_account_id", ForeignKey("user_account.user_account_id")),
    Column("tweet_id", ForeignKey("tweet.tweet_id")),
)
