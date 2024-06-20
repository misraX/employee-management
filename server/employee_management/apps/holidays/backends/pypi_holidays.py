from datetime import date, datetime
from typing import Tuple

from holidays import country_holidays

from server.employee_management.apps.holidays.backends.backend import HolidaysBackend


class PyPiHolidaysBackend(HolidaysBackend):
    """
    PyPi Holidays Backend, retrieve the data from https://pypi.org/project/holidays/
    """

    def get_holidays(
        self,
        country: str,
        years: list[datetime.year],
        categories: Tuple[str],
        language: str = "en_US",
    ) -> list[tuple[date, str]] | None:
        holidays = country_holidays(
            country=country, years=years, categories=categories, language=language
        )
        if not holidays:
            return None
        holidays_items = holidays.items()

        return sorted(holidays_items, key=lambda item: item[1], reverse=True)
