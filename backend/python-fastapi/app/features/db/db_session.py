from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.common.base.base_config import DATABASE_URL, RESOURCES_DIR

session_context: ContextVar[str] = ContextVar(
    "session_context", default="No changes at all"
)


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


# engines = {
#     "writer": create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
#     "reader": create_async_engine(config.READER_DB_URL, pool_recycle=3600),
# }
# engines = {
#     "writer": create_async_engine(DATABASE_URL, pool_recycle=3600),
#     "reader": create_async_engine(DATABASE_URL, pool_recycle=3600),
# }
engine = create_async_engine(DATABASE_URL, pool_recycle=3600)


# class RoutingSession(Session):
#     def get_bind(self, mapper=None, clause=None, **kw):
#         if self._flushing or isinstance(clause, (Update, Delete, Insert)):
#             return engines["writer"].sync_engine
#         else:
#             return engines["reader"].sync_engine


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        return engine.sync_engine
        # if self._flushing or isinstance(clause, (Update, Delete, Insert)):
        #     return engines["writer"].sync_engine
        # else:
        #     return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
)
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)
# Base = declarative_base()
BaseTableObject = declarative_base()
DATABASE_URL: str = "sqlite:///" + RESOURCES_DIR + "\\twitter.db"

######################################

sync_engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar("db_session")
