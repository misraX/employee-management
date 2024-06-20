import abc
from datetime import date, datetime
from typing import Generic, Tuple, TypeVar

T = TypeVar("T")


class HolidaysBackend(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def get_holidays(
        self, country: str, years: list[datetime.year], categories: Tuple[str]
    ) -> list[tuple[date, str]] | None:
        pass
