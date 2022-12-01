from datetime import datetime

from sqlalchemy.orm import Session

from app.common.util.log_util import log
from app.features.user_account.user_account import UserAccount
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import (
    UserAccountResponse,
    UserAccountSignUpRequest,
)


class UserAccountService:
    def __init__(self):
        self.user_account_repository = UserAccountRepository()

    def sign_up(
        self, session: Session, user_account_sign_up_request: UserAccountSignUpRequest
    ) -> UserAccountResponse:
        user_account = UserAccount()
        user_account.email = user_account_sign_up_request.email
        user_account.password = user_account_sign_up_request.password
        user_account.username = user_account_sign_up_request.username
        user_account.joined_date = datetime.now()

        session.add(user_account)
        session.commit()

        user_account_response = UserAccountResponse.from_orm(user_account)
        return user_account_response

    def get_by_username(self, session: Session, username: str) -> UserAccountResponse:
        user_account = self.user_account_repository.get_by_username(
            session=session, username=username
        )
        user_account_response = UserAccountResponse.from_orm(user_account)
        return user_account_response

    def get_list_of_followers_by_username(
        self, session: Session, username: str
    ) -> list[UserAccountResponse]:
        user_accounts = self.user_account_repository.get_list_of_followers_by_username(
            session=session, username=username
        )
        return [UserAccountResponse.from_orm(x) for x in user_accounts]

    def get_list_of_following_by_username(
        self, session: Session, username: str
    ) -> list[UserAccountResponse]:
        user_accounts = self.user_account_repository.get_list_of_following_by_username(
            session=session, username=username
        )
        return [UserAccountResponse.from_orm(x) for x in user_accounts]
