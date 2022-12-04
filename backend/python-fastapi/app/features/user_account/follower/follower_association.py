from sqlalchemy import Column, ForeignKey, Table

from app.features.db.database import BaseModel

Follower = Table(
    "follower",
    BaseModel.metadata,
    Column("follower_id", ForeignKey("user_account.user_account_id")),
    Column("followee_id", ForeignKey("user_account.user_account_id")),
)
