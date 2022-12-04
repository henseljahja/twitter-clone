from fastapi import APIRouter, Depends

from app.features.security.security_service import SecurityService
from app.features.user_account.user_account_schema import (
    UserAccountResponse,
    UserAccountSignUpRequest,
)
from app.features.user_account.user_account_service import UserAccountService

user_account_service = UserAccountService()
user_account_controller = APIRouter()
security_service = SecurityService()


@user_account_controller.post(
    "/signUp",
    response_model=UserAccountResponse,
    response_model_exclude_none=True,
)
def sign_up(
    *, user_account_sign_up_request: UserAccountSignUpRequest
) -> UserAccountResponse:

    return user_account_service.sign_up(
        user_account_sign_up_request=user_account_sign_up_request
    )


@user_account_controller.get(
    "/username/{username}",
    response_model=UserAccountResponse,
    response_model_exclude_none=True,
)
def get_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
):
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )
    return user_account_service.get_by_username(username=username)


@user_account_controller.get(
    "/username/{username}/followers",
    response_model=list[UserAccountResponse],
    response_model_exclude_none=True,
)
def get_list_of_followers_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
):
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )
    return user_account_service.get_list_of_followers_by_username(username=username)


@user_account_controller.get(
    "/username/{username}/following",
    response_model=list[UserAccountResponse],
    response_model_exclude_none=True,
)
def get_list_of_following_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
):
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )
    return user_account_service.get_list_of_following_by_username(username=username)
