from sqlalchemy import Column, ForeignKey, Table

from app.features.db.database import BaseModel

Reply = Table(
    "reply",
    BaseModel.metadata,
    Column("reply_id", ForeignKey("tweet.tweet_id")),
    Column("tweet_id", ForeignKey("tweet.tweet_id")),
)
