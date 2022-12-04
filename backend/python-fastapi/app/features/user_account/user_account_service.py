from datetime import datetime

from fastapi import HTTPException
from starlette import status

from app.features.user_account.follower.follower_repository import FollowerRepository
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import (
    UserAccountResponse,
    UserAccountSignUpRequest,
)


class UserAccountService:
    def __init__(self):
        self.user_account_repository = UserAccountRepository()
        self.follower_repository = FollowerRepository()

    def check_privilege_by_username(
        self, user_account: UserAccountResponse, username: str
    ) -> bool:
        if user_account.username == username:
            return True
        if self.user_account_repository.is_user_account_private(username=username):
            if not self.user_account_repository.is_follower(
                user_account=user_account, username=username
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="NOT A FOLLOWER. UNABLE TO VIEW",
                )
        return True

    def sign_up(
        self, user_account_sign_up_request: UserAccountSignUpRequest
    ) -> UserAccountResponse:
        user_account = UserAccount()
        user_account.email = user_account_sign_up_request.email
        user_account.password = user_account_sign_up_request.password
        user_account.username = user_account_sign_up_request.username
        user_account.joined_date = datetime.now()

        user_account = self.user_account_repository.create(user_account)

        user_account_response = UserAccountResponse.from_orm(user_account)
        return user_account_response

    def get_by_username(self, username: str) -> UserAccountResponse:
        user_account = self.user_account_repository.get_by_username(username=username)
        user_account_response = UserAccountResponse.from_orm(user_account)
        return user_account_response

    def get_list_of_followers_by_username(
        self, username: str
    ) -> list[UserAccountResponse]:
        user_accounts = self.user_account_repository.get_list_of_followers_by_username(
            username=username
        )
        return [UserAccountResponse.from_orm(x) for x in user_accounts]

    def get_list_of_following_by_username(
        self, username: str
    ) -> list[UserAccountResponse]:
        user_accounts = self.user_account_repository.get_list_of_following_by_username(
            username=username
        )
        return [UserAccountResponse.from_orm(x) for x in user_accounts]

    def is_private(self, username: str) -> bool:
        return self.user_account_repository.is_user_account_private(username=username)

    def is_follower(self, requester_username: str, target_username: str) -> bool:
        requester_user_account = self.get_by_username(username=requester_username)
        target_user_account = self.get_by_username(username=target_username)
        return self.follower_repository.is_follower(
            requester_user_account_id=requester_user_account.user_account_id,
            target_user_account_id=target_user_account.user_account_id,
        )
