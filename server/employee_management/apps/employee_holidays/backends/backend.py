import abc
from datetime import date, datetime
from typing import Generic, Tuple, TypeVar

T = TypeVar("T")


class HolidaysBackend(abc.ABC, Generic[T]):
    """
    Base class for all employee_holidays backends.
    """

    @abc.abstractmethod
    def get_holidays(
        self, country: str, years: list[datetime.year], categories: Tuple[str], language: str
    ) -> list[tuple[date, str]] | None:
        pass
