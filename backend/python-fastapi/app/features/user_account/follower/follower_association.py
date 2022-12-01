from sqlalchemy import Column, ForeignKey, Table

from app.common.base.base_config import BaseTableObject

Follower = Table(
    "follower",
    BaseTableObject.metadata,
    Column("follower_id", ForeignKey("user_account.user_account_id")),
    Column("followee_id", ForeignKey("user_account.user_account_id")),
)