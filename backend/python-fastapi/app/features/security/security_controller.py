from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.features.security.security_schema import LoginResponse
from app.features.security.security_service import SecurityService
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import UserAccountResponse

security_controller = APIRouter()
user_account_repository = UserAccountRepository()
security_service = SecurityService()


@security_controller.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=LoginResponse,
    response_model_exclude_none=True,
)
async def login(
    *,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_account_repository.get_by_username(username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username doesn't exist",
        )

    if not security_service.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    return LoginResponse(
        access_token=security_service.create_access_token(user.email),
        refresh_token=security_service.create_refresh_token(user.email),
    )


@security_controller.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserAccountResponse,
    response_model_exclude_none=True,
)
async def get_me(
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
):
    return user_account
