from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.features.db.database import BaseModel
from app.features.tweet.quote_retweet.quote_retweet_association import QuoteRetweet
from app.features.tweet.reply.reply_association import Reply


class Tweet(BaseModel):
    __tablename__ = "tweet"
    tweet_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    source = Column(String)
    created_date = Column(DateTime)
    user_account_id = Column(Integer, ForeignKey("user_account.user_account_id"))
    user_account = relationship("UserAccount", back_populates="tweet")
    reply = relationship(
        "Tweet",
        secondary=Reply,
        primaryjoin=Reply.c.tweet_id == tweet_id,
        secondaryjoin=Reply.c.reply_id == tweet_id,
    )
    quote_retweet = relationship(
        "Tweet",
        secondary=QuoteRetweet,
        primaryjoin=QuoteRetweet.c.tweet_id == tweet_id,
        secondaryjoin=QuoteRetweet.c.quote_retweet_id == tweet_id,
    )
