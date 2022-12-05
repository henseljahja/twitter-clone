import os

from app.common.base.base_config import RESOURCES_DIR, base_config

# Database settings
DATABASE_URL: str = "sqlite:///" + RESOURCES_DIR + "\\twitter.db"

INITIAL_DATA_DIR: str = os.path.join(RESOURCES_DIR, "sql")


DB_DROP_TABLES: bool = base_config("DB_DROP_TABLES", cast=bool, default=False)
DB_CREATE: bool = base_config("DB_CREATE", cast=bool, default=False)
DB_DUMMY_DATA: bool = base_config("DB_DUMMY_DATA", cast=bool, default=False)
