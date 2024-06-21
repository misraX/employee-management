import abc
from datetime import date, datetime
from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")


class HolidaysBackend(abc.ABC, Generic[T]):
    """
    Base class for all employee_holidays backends.
    """

    @abc.abstractmethod
    def get_holidays(
        self, country: str, years: list[datetime.year], categories: Tuple[str], language: str
    ) -> List[tuple[date, str]] | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_week_holidays(
        self, country: str, categories: Tuple[str], language: str = "en_US"
    ) -> List[Tuple[date, str]] | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_upcoming_holidays(
        self, country: str, categories: Tuple[str], language: str = "en_US"
    ) -> List[Tuple[date, str]] | None:
        raise NotImplementedError
