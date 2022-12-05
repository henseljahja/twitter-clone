import os

from app.common.base.log_config import log
from app.features.db.database import BaseModel, sync_engine
from app.features.db.db_config import (  # ENGINE,; BaseTableObject,; SessionMaker,
    INITIAL_DATA_DIR,
)
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount

tables = [UserAccount, Tweet]


def create_database() -> None:
    BaseModel.metadata.create_all(bind=sync_engine)


def execute_sql_scripts(filename: str) -> None:
    if filename.endswith(".sql"):
        try:
            sql_file = open(filename, "r", encoding="utf-8").read()
            with sync_engine.begin() as conn:
                try:
                    new_conn = conn.connection
                    new_conn.executescript(sql_file)
                except Exception as e:
                    print(e)
                    raise

        except Exception as e:
            log.error(
                f"{__name__} | Error: failed to execute sql file: "
                + filename
                + " | "
                + str(e)
            )


def init_data():
    try:
        dummy_data_files = os.listdir(INITIAL_DATA_DIR)
        dummy_data_files.sort()
        for sql_file in dummy_data_files:
            execute_sql_scripts(os.path.join(INITIAL_DATA_DIR, sql_file))
        log.info("Dummy data loaded")
    except Exception as e:
        log.error(f"{__name__} | Failed to insert data into database: {e}")


def drop_tables() -> None:
    try:
        BaseModel.metadata.drop_all(bind=sync_engine)
    except Exception as e:
        log.error(f"{__name__} | Failed to drop tables : {e}")
