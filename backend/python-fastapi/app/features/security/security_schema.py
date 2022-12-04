from __future__ import annotations

from tkinter.tix import Form
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.common.base.base_schema import BaseSchema


class LoginResponse(BaseModel):
    access_token: str | None
    refresh_token: str | None
    token_type: str = "Bearer"


class TokenResponse(BaseSchema):
    exp: int
    email: str
