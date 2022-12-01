from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.util import db_util
from app.features.user_account.user_account_schema import (
    UserAccountResponse,
    UserAccountSignUpRequest,
)
from app.features.user_account.user_account_service import UserAccountService

user_account_service = UserAccountService()
user_account_controller = APIRouter()


@user_account_controller.post(
    "/signUp",
    response_model=UserAccountResponse,
    response_model_exclude_none=True,
)
def sign_up(
    *,
    session: Session = Depends(db_util.get_session),
    user_account_sign_up_request: UserAccountSignUpRequest
) -> UserAccountResponse:
    return user_account_service.sign_up(
        session=session, user_account_sign_up_request=user_account_sign_up_request
    )


@user_account_controller.get(
    "/username/{username}",
    response_model=UserAccountResponse,
    response_model_exclude_none=True,
)
def get_by_username(*, session: Session = Depends(db_util.get_session), username: str):
    return user_account_service.get_by_username(session=session, username=username)


@user_account_controller.get(
    "/username/{username}/followers",
    response_model=list[UserAccountResponse],
    response_model_exclude_none=True,
)
def get_list_of_followers_by_username(
    *, session: Session = Depends(db_util.get_session), username: str
):
    return user_account_service.get_list_of_followers_by_username(
        session=session, username=username
    )


@user_account_controller.get(
    "/username/{username}/following",
    response_model=list[UserAccountResponse],
    response_model_exclude_none=True,
)
def get_list_of_following_by_username(
    *, session: Session = Depends(db_util.get_session), username: str
):
    return user_account_service.get_list_of_following_by_username(
        session=session, username=username
    )
