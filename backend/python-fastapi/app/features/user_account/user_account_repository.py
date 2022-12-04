from sqlalchemy import and_, select

from app.features.db.db_session import session
from app.features.db.transactional import Transactional
from app.features.user_account.follower.follower_association import Follower
from app.features.user_account.follower.follower_repository import FollowerRepository
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_schema import UserAccountResponse


class UserAccountRepository:
    def __init__(self):
        self.follower_repository = FollowerRepository()

    async def get_by_username(self, username: str) -> UserAccount:
        user_account = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )
        return user_account

    async def get_by_email(self, email: str) -> UserAccount:

        user_account = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.email == email)
                    )
                )
            )
            .scalars()
            .first()
        )
        return user_account

    async def get_list_of_followers_by_username(
        self, username: str
    ) -> list[UserAccount]:
        user_account_id_to_search = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )
        user_accounts = (
            (
                await (
                    session.execute(
                        select(UserAccount)
                        .join(
                            Follower,
                            and_(UserAccount.user_account_id == Follower.c.follower_id),
                        )
                        .filter(
                            Follower.c.followee_id
                            == user_account_id_to_search.user_account_id
                        )
                    )
                )
            )
            .scalars()
            .all()
        )
        return user_accounts

    async def get_list_of_following_by_username(
        self, username: str
    ) -> list[UserAccount]:
        user_account_id_to_search = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )
        user_accounts = (
            (
                await (
                    session.execute(
                        select(UserAccount)
                        .join(
                            Follower,
                            and_(UserAccount.user_account_id == Follower.c.followee_id),
                        )
                        .filter(
                            Follower.c.follower_id
                            == user_account_id_to_search.user_account_id
                        )
                    )
                )
            )
            .scalars()
            .all()
        )
        return user_accounts

    async def get_list_of_user_accounts(self) -> list[UserAccount]:
        user_accounts = (await (session.execute(select(UserAccount)))).scalars().all()
        return user_accounts

    async def is_user_account_private(self, username: str) -> bool:
        user_account = (
            (
                await (
                    session.execute(
                        select(UserAccount).filter(UserAccount.username == username)
                    )
                )
            )
            .scalars()
            .first()
        )

        return user_account.is_private

    async def is_follower(
        self, user_account: UserAccountResponse, username: str
    ) -> bool:
        user_account = await self.get_by_username(username=username)

        return await self.follower_repository.is_follower(
            requester_user_account_id=user_account.user_account_id,
            target_user_account_id=user_account.user_account_id,
        )

    @Transactional()
    async def create(self, user_account: UserAccount) -> UserAccount:
        session.add(user_account)
        return user_account
