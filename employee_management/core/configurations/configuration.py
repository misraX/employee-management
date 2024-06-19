import os
import pathlib
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


class Configuration:
    @property
    def base_dir(self) -> pathlib.Path:
        """
        Base directory for all configuration files

        :return: pathlib.Path
        """
        return BASE_DIR

    @property
    def database_url(self) -> str:
        """
        Database URL if the url is configured with in-memory database no transformation
        will be applied otherwise the database url will be a join of base_dir and the DATABASE_URL

        :return: str
        """
        database_url_from_env = os.getenv("DATABASE_URL")
        if database_url_from_env != ":memory:":
            return os.path.join(self.base_dir, os.getenv("DATABASE_URL"))
        return database_url_from_env

    @property
    def app_name(self) -> str:
        """
        Application name getter from the environment variables

        :return: str
        """
        return os.getenv("APP_NAME")


@lru_cache
def configuration() -> Configuration:
    return Configuration()
