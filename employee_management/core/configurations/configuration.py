import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


class Configuration:
    @property
    def base_dir(self):
        return BASE_DIR

    @property
    def database_url(self):
        return os.path.join(self.base_dir, os.getenv("DATABASE_URL"))

    @property
    def app_name(self) -> str:
        return os.getenv("APP_NAME")


@lru_cache
def configuration() -> Configuration:
    return Configuration()
