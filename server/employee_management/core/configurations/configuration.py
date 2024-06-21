import os
import pathlib
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


class Configuration:
    @property
    def logging_level(self):
        return os.getenv("LOGGING_LEVEL", "INFO")

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
        if not database_url_from_env.startswith(":memory:"):
            return os.path.join(self.base_dir, os.getenv("DATABASE_URL"))
        return database_url_from_env

    @property
    def app_name(self) -> str:
        """
        Application name getter from the environment variables

        :return: str
        """
        return os.getenv("APP_NAME")

    @property
    def smtp_server(self) -> str:
        return os.getenv("SMTP_SERVER")

    @property
    def smtp_port(self) -> int:
        return int(os.getenv("SMTP_PORT"))

    @property
    def smtp_user(self) -> str:
        return os.getenv("SMTP_USER")

    @property
    def smtp_password(self) -> str:
        return os.getenv("SMTP_PASSWORD")


@lru_cache
def get_configuration() -> Configuration:
    return Configuration()


configuration = get_configuration()
