from datetime import datetime
from typing import List, Tuple

from server.employee_management.apps.employee_holidays.backends.backend import HolidaysBackend
from server.employee_management.apps.employee_holidays.backends.pypi_holidays import (
    PyPiHolidaysBackend,
)


class EmployeeHolidayService:
    def __init__(self, holidays_backend: HolidaysBackend = PyPiHolidaysBackend):
        self.holidays_backend = holidays_backend

    def get_holidays(
        self,
        country: str,
        years: List[datetime.year],
        categories: Tuple[str],
        language: str = "en_US",
    ) -> List | None:
        return self.holidays_backend.get_holidays(
            country=country, years=years, categories=categories, language=language
        )
