from sqlalchemy import and_, func

from app.common.base.log_config import log
from app.features.db.database import db
from app.features.tweet.tweet import Tweet
from app.features.user_account.follower.follower_association import Follower
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_schema import UserAccountResponse


class UserAccountRepository:
    def __init__(self):
        ...

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
        is_follower = (
            db.session.query(Follower)
            .filter(
                Follower.c.follower_id == user_account.user_account_id,
                Follower.c.followee_id == user_account_id,
            )
            .first()
        )
        if is_follower is None:
            return False
        return True

    def create(self, user_account: UserAccount) -> UserAccount:
        db.session.add(user_account)
        db.session.commit()
        db.session.refresh(user_account)
        return user_account

    def get_user_account_by_tweet_id(self, tweet_id: int) -> UserAccount:
        user_account = (
            db.session.query(UserAccount)
            .join(Tweet)
            .filter(Tweet.tweet_id == tweet_id)
            .first()
        )
        return user_account

    def is_follower(
        self,
        requester_user_account_id: int,
        target_user_account_id: int,
    ):
        is_follower = (
            db.session.query(Follower)
            .filter(
                Follower.c.follower_id == requester_user_account_id,
                Follower.c.followee_id == target_user_account_id,
            )
            .first()
        )
        if is_follower is None:
            return False
        return True

    def get_count_following_by_user_account_id(self, user_account_id: int) -> int:
        count_following = (
            db.session.query(func.count(Follower.c.followee_id))
            .filter(Follower.c.followee_id == user_account_id)
            .scalar()
        )
        log.debug(f"count_following => {count_following}")

        return count_following

    def get_count_follower_by_user_account_id(self, user_account_id: int) -> int:
        count_follower = (
            db.session.query(func.count(Follower.c.follower_id))
            .filter(Follower.c.follower_id == user_account_id)
            .scalar()
        )
        log.debug(f"Count follower => {count_follower}")
        return count_follower
