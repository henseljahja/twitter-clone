from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.features.security.security_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_SECRET_KEY,
)
from app.features.security.security_schema import TokenResponse
from app.features.user_account.user_account_repository import UserAccountRepository
from app.features.user_account.user_account_schema import UserAccountResponse

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


class SecurityService:
    def __init__(self):
        self.user_account_repository = UserAccountRepository()
        ...

    def get_hashed_password(self, password: str) -> str:
        return password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    def create_access_token(
        self, subject: Union[str, Any], expires_delta: int = None
    ) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expires_delta, "email": str(subject)}
        encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
        self, subject: Union[str, Any], expires_delta: int = None
    ) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(
                minutes=REFRESH_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expires_delta, "email": str(subject)}
        encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self, token: str = Depends(reuseable_oauth)
    ) -> UserAccountResponse:
        try:
            payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenResponse(**payload)
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_account = await self.user_account_repository.get_by_email(
            email=token_data.email
        )
        if user_account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        user_account.password = None
        return UserAccountResponse.from_orm(user_account)
