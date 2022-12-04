from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.common.base.base_config import DB_CREATE, DB_DROP_TABLES, DB_DUMMY_DATA
from app.common.util import db_util
from app.features.security.security_controller import security_controller
from app.features.tweet.tweet_controller import tweet_controller
from app.features.user_account.user_account_controller import user_account_controller

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_account_controller)
app.include_router(router=tweet_controller)
app.include_router(router=security_controller)


@app.on_event("startup")
async def startup_event():
    if DB_DROP_TABLES:
        db_util.drop_tables()
    if DB_CREATE:
        db_util.create_database()
    if DB_DUMMY_DATA:
        db_util.init_data()
