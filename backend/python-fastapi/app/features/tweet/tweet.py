from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.features.db.database import BaseModel


class Tweet(BaseModel):
    __tablename__ = "tweet"
    tweet_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    source = Column(String)
    created_date = Column(DateTime)
    user_account_id = Column(Integer, ForeignKey("user_account.user_account_id"))
    user_account = relationship("UserAccount", back_populates="tweet", lazy="noload")
