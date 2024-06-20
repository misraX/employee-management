from datetime import date, datetime, timedelta
from typing import List, Tuple

from holidays import country_holidays

from server.employee_management.apps.employee_holidays.backends.backend import HolidaysBackend


class PyPiHolidaysBackend(HolidaysBackend):
    """
    PyPi Holidays Backend, retrieve the data from https://pypi.org/project/holidays/
    """

    def get_holidays(
        self,
        country: str,
        years: List[datetime.year],
        categories: Tuple[str],
        language: str = "en_US",
    ) -> List[tuple[date, str]] | None:
        """
        Get holidays for a given country, years, categories and language.


        :param country: string, the name of the country code
        :param years: list of years as integers
        :param categories: list of categories as strings ['public', 'bank']
        :param language: string, the code of the language (default is 'en_US')
        :return: A list of tuples containing the date and name of each holiday or None
        """
        holidays = country_holidays(
            country=country, years=years, categories=categories, language=language
        )
        if not holidays:
            return None
        holidays_items = holidays.items()

        return sorted(holidays_items, key=lambda item: item[1], reverse=True)

    def get_current_week_holidays(
        self, country: str, categories: Tuple[str], language: str = "en_US"
    ) -> List[Tuple[date, str]] | None:
        """
        Get holidays for the current week.

        :param country: The country code for which to retrieve holidays.
        :param categories: A tuple of categories as strings.
        :param language: The language code (default is 'en_US').
        :return: A list of tuples containing the date and name of each holiday or None
        """
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        holidays = self.get_holidays(
            country=country, years=[today.year], categories=categories, language=language
        )
        if not holidays:
            return None

        current_week_holidays = [
            (holiday_date, name)
            for holiday_date, name in holidays
            if start_of_week <= holiday_date <= end_of_week
        ]

        return sorted(current_week_holidays, key=lambda item: item[0])

    def get_upcoming_holidays(
        self, country: str, categories: Tuple[str], language: str = "en_US"
    ) -> List[Tuple[date, str]] | None:
        """
        Get holidays in the next 7 days if today is Monday.

        :param country: The country code for which to retrieve holidays.
        :param categories: A tuple of categories as strings.
        :param language: The language code (default is 'en_US').
        :return: A list of tuples containing the date and name of each holiday or None
        """
        today = date.today()
        if today.weekday() != 0:  # Not Monday
            return None

        next_seven_days = today + timedelta(days=7)

        holidays = self.get_holidays(
            country=country, years=[today.year], categories=categories, language=language
        )
        if not holidays:
            return None

        upcoming_holidays = [
            (holiday_date, name)
            for holiday_date, name in holidays
            if today <= holiday_date <= next_seven_days
        ]

        return sorted(upcoming_holidays, key=lambda item: item[0])
