import os
from typing import Any

from sqlalchemy.orm import Session

from app.common.base.base_config import (  # ENGINE,; BaseTableObject,; SessionMaker,
    INITIAL_DATA_DIR,
)
from app.common.base.log_config import log
from app.features.db.database import BaseModel, sync_engine
from app.features.tweet.tweet import Tweet
from app.features.user_account.user_account import UserAccount

tables = [UserAccount, Tweet]


def create_database() -> None:
    # def init_models():
    #     with engine.begin() as conn:
    #         await conn.run_sync(BaseTableObject.metadata.drop_all)
    #         await conn.run_sync(BaseTableObject.metadata.create_all)
    #
    # asyncio.run(init_models())
    BaseModel.metadata.create_all(bind=sync_engine)


def execute_sql_scripts(filename: str, engine: Any) -> None:
    if filename.endswith(".sql"):
        try:
            sql_file = open(filename, "r")
            escaped_sql = sql_file.read()
            escaped_sql = escaped_sql.split("\n")
            for i in escaped_sql:
                with Session(sync_engine) as session:
                    try:
                        session.execute(i)
                        session.commit()
                    except Exception as e:
                        print(e)
                        session.rollback()
                        raise
                    finally:
                        session.close()
            sql_file.close()

        except Exception as e:
            log.error(
                f"{__name__} | Error: failed to execute sql file: "
                + filename
                + " | "
                + str(e)
            )


def init_data() -> None:
    try:
        dummy_data_files = os.listdir(INITIAL_DATA_DIR)
        dummy_data_files.sort()
        for sql_file in dummy_data_files:
            execute_sql_scripts(os.path.join(INITIAL_DATA_DIR, sql_file), sync_engine)
        log.info("Dummy data loaded")
    except Exception as e:
        log.error(f"{__name__} | Failed to insert data into database: {e}")


def drop_tables() -> None:
    try:
        BaseModel.metadata.drop_all(bind=sync_engine)
    except Exception as e:
        log.error(f"{__name__} | Failed to drop tables : {e}")
