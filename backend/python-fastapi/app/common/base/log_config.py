import logging
from logging.config import dictConfig

from pydantic import BaseModel

from app.common.base.base_config import base_config

LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
LOGGER_NAME: str = "main"
LOG_LEVEL: str = base_config("LOG_LEVEL", cast=str, default="DEBUG")
APP_NAME: str = "LIVENESS"


class LogConfig(BaseModel):

    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "main": {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
log = logging.getLogger("main")
