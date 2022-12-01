from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.common.base.base_config import BaseTableObject
from app.features.retweet.retweet_association import Retweet
from app.features.user_account.follower.follower_association import Follower


class UserAccount(BaseTableObject):
    __tablename__ = "user_account"
    user_account_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    about = Column(String)
    categories = Column(String)
    location = Column(String)
    website = Column(String)
    joined_date = Column(DateTime)
    birthdate = Column(DateTime)
    is_verified = Column(Boolean)
    is_private = Column(Boolean)
    is_official_account = Column(Boolean)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String)
    country = Column(String)
    tweet = relationship("Tweet", back_populates="user_account", lazy="noload")
    follower = relationship(
        "UserAccount",
        secondary=Follower,
        primaryjoin=Follower.c.followee_id == user_account_id,
        secondaryjoin=Follower.c.follower_id == user_account_id,
    )
    retweet = relationship("UserAccount", secondary=Retweet)
