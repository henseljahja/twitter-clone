import os
from pathlib import Path

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
