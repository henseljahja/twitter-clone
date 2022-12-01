import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from starlette.config import Config

ROOT_DIR = os.path.dirname(Path(__file__).resolve().parents[2])
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

base_config: Config = Config(os.path.join(RESOURCES_DIR, ".env"))

SERVER_HOST: str = base_config("SERVER_HOST", cast=str, default="0.0.0.0")
SERVER_PORT: int = base_config("SERVER_PORT", cast=int, default=9001)
NUMBER_OF_WORKERS: int = base_config("NUMBER_OF_WORKERS", cast=int, default=9)

# Development Config
DEBUG: bool = base_config("DEBUG", cast=bool, default=True)
RELOAD: bool = base_config("RELOAD", cast=bool, default=True)

# Database settings
DATABASE_URL: str = "sqlite:///" + RESOURCES_DIR + "\\twitter.db"

INITIAL_DATA_DIR: str = os.path.join(RESOURCES_DIR, "sql")


DB_DROP_TABLES: bool = base_config("DB_DROP_TABLES", cast=bool, default=False)
DB_CREATE: bool = base_config("DB_CREATE", cast=bool, default=False)
DB_DUMMY_DATA: bool = base_config("DB_DUMMY_DATA", cast=bool, default=False)

ENGINE = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

BaseTableObject = declarative_base()
SessionMaker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE,
)
