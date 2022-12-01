from sqlalchemy import and_
from sqlalchemy.orm import Session, subqueryload

from app.common.util.log_util import log
from app.features.user_account import follower
from app.features.user_account.follower.follower_association import Follower
from app.features.user_account.user_account import UserAccount


class UserAccountRepository:
    def get_by_username(self, session: Session, username: str) -> UserAccount:
        user_account = (
            session.query(UserAccount).filter(UserAccount.username == username).first()
        )
        return user_account

    def get_list_of_followers_by_username(
        self, session: Session, username: str
    ) -> list[UserAccount]:
        user_account_id_to_search = (
            session.query(UserAccount).filter(UserAccount.username == username).first()
        )
        user_accounts = (
            session.query(UserAccount)
            .join(Follower, and_(UserAccount.user_account_id == Follower.c.follower_id))
            .filter(Follower.c.followee_id == user_account_id_to_search.user_account_id)
            .all()
        )
        return user_accounts

    def get_list_of_following_by_username(
        self, session: Session, username: str
    ) -> list[UserAccount]:
        user_account_id_to_search = (
            session.query(UserAccount).filter(UserAccount.username == username).first()
        )
        user_accounts = (
            session.query(UserAccount)
            .join(Follower, and_(UserAccount.user_account_id == Follower.c.followee_id))
            .filter(Follower.c.follower_id == user_account_id_to_search.user_account_id)
            .all()
        )
        return user_accounts
