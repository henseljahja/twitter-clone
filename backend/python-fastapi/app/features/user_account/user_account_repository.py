from sqlalchemy import and_

from app.features.db.database import db
from app.features.user_account.follower.follower_association import Follower
from app.features.user_account.follower.follower_repository import FollowerRepository
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_schema import UserAccountResponse


class UserAccountRepository:
    def __init__(self):
        self.follower_repository = FollowerRepository()

    def get_by_username(self, username: str) -> UserAccount:
        user_account = (
            db.session.query(UserAccount)
            .filter(UserAccount.username == username)
            .first()
        )
        return user_account

    def get_by_email(self, email: str) -> UserAccount:

        user_account = (
            db.session.query(UserAccount).filter(UserAccount.email == email).first()
        )
        return user_account

    def get_list_of_followers_by_username(self, username: str) -> list[UserAccount]:
        user_account_id_to_search = (
            db.session.query(UserAccount)
            .filter(UserAccount.username == username)
            .first()
        )
        user_accounts = (
            db.session.query(UserAccount)
            .join(
                Follower,
                and_(UserAccount.user_account_id == Follower.c.follower_id),
            )
            .filter(Follower.c.followee_id == user_account_id_to_search.user_account_id)
            .all()
        )
        return user_accounts

    def get_list_of_following_by_username(self, username: str) -> list[UserAccount]:
        user_account_id_to_search = self.get_by_username(username=username)
        user_accounts = (
            db.session.query(UserAccount)
            .join(
                Follower,
                and_(UserAccount.user_account_id == Follower.c.followee_id),
            )
            .filter(Follower.c.follower_id == user_account_id_to_search.user_account_id)
            .all()
        )
        return user_accounts

    def get_list_of_user_accounts(self) -> list[UserAccount]:
        user_accounts = db.session.query(UserAccount).all()
        return user_accounts

    def is_user_account_private(self, username: str) -> bool:
        user_account = (
            db.session.query(UserAccount)
            .filter(UserAccount.username == username)
            .first()
            .is_private
        )

        return user_account

    def is_follower(self, user_account: UserAccountResponse, username: str) -> bool:
        user_account_id = self.get_by_username(username=username).user_account_id
        return self.follower_repository.is_follower(
            requester_user_account_id=user_account.user_account_id,
            target_user_account_id=user_account_id,
        )

    def create(self, user_account: UserAccount) -> UserAccount:
        db.session.add(user_account)
        db.session.commit()
        db.session.refresh(user_account)
        return user_account
