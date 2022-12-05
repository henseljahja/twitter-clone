from sqlalchemy import Column, ForeignKey, Table

from app.features.db.database import BaseModel

QuoteRetweet = Table(
    "quote_retweet",
    BaseModel.metadata,
    Column("quote_retweet_id", ForeignKey("tweet.tweet_id")),
    Column("tweet_id", ForeignKey("tweet.tweet_id")),
)
