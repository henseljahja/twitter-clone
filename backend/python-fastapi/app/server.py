from typing import Any, Callable, Coroutine

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.common.base.base_config import DB_CREATE, DB_DROP_TABLES, DB_DUMMY_DATA
from app.common.util import db_util
from app.common.util.db_util import SessionMaker
from app.features.tweet.tweet_controller import tweet_controller
from app.features.user_account.user_account_controller import user_account_controller


def startup_handler(
    app: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        if DB_DROP_TABLES:
            db_util.drop_tables()
        if DB_CREATE:
            db_util.create_database()
        if DB_DUMMY_DATA:
            db_util.init_data()

    return start_app


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_event_handler("startup", startup_handler)

app.include_router(router=user_account_controller)
app.include_router(router=tweet_controller)
