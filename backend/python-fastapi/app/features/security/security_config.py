from app.common.base.base_config import base_config

ACCESS_TOKEN_EXPIRE_MINUTES = base_config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30
)
REFRESH_TOKEN_EXPIRE_MINUTES = base_config(
    "REFRESH_TOKEN_EXPIRE_MINUTES", cast=int, default=10080
)  # 7 days
ALGORITHM = base_config("ALGORITHM", cast=str, default="HS256")
ACCESS_TOKEN_SECRET_KEY = base_config(
    "ACCESS_TOKEN_SECRET_KEY", cast=str, default="secret"
)
REFRESH_TOKEN_SECRET_KEY = base_config(
    "REFRESH_TOKEN_SECRET_KEY", cast=str, default="secret"
)
