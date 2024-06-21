import unittest
from datetime import date
from unittest.mock import patch

from faker import Faker
from holidays import PUBLIC

from server.employee_management.apps.employee_holidays.backends.pypi_holidays import (
    PyPiHolidaysBackend,
)

faker = Faker()


class PyPiHolidaysTests(unittest.TestCase):
    def setUp(self):
        self.country = "SV"
        self.holiday_category = PUBLIC
        self.holiday_years = [2023]
        self.backend = PyPiHolidaysBackend()

    def test_pypi_holidays(self):
        get_holidays = self.backend.get_holidays(
            country=self.country, years=self.holiday_years, categories=(self.holiday_category,)
        )
        for holiday in get_holidays:
            self.assertEqual(holiday[0].year, self.holiday_years[0])

    @patch(
        "server.employee_management.apps.employee_holidays.backends.pypi_holidays.country_holidays"
    )
    def test_get_holidays_no_holidays(self, mock_country_holidays):
        mock_country_holidays.return_value = {}

        holidays = self.backend.get_holidays(
            country="US", years=[2024], categories=("public",), language="en_US"
        )

        self.assertIsNone(holidays)

    @patch(
        "server.employee_management.apps.employee_holidays.backends.pypi_holidays.country_holidays"
    )
    def test_get_holidays(self, mock_country_holidays):
        mock_country_holidays.return_value = {
            date(2024, 1, 1): "New Year's Day",
            date(2024, 12, 25): "Christmas Day",
        }

        holidays = self.backend.get_holidays(
            country="US", years=[2024], categories=("public",), language="en_US"
        )

        expected_holidays = [
            (date(2024, 1, 1), "New Year's Day"),
            (date(2024, 12, 25), "Christmas Day"),
        ]

        self.assertEqual(holidays, expected_holidays)

    @patch(
        "server.employee_management.apps.employee_holidays.backends.pypi_holidays.country_holidays"
    )
    def test_get_current_week_holidays(self, mock_country_holidays):
        mock_country_holidays.return_value = {
            date(2024, 5, 1): "The Labour Day",
            date(2024, 5, 6): "Sham El-Nassim",
            date(2024, 6, 30): "30 June Revolution",
        }
        with patch(
            "server.employee_management.apps.employee_holidays.backends.pypi_holidays.date"
        ) as mock_holidays:
            mock_holidays.today.return_value = date(2024, 4, 30)
            # The start of the week will be datetime.date(2024, 4, 29)
            # and end of week will be datetime.date(2024, 5, 5)
            holidays = self.backend.get_current_week_holidays(
                country=self.country,
                categories=(self.holiday_category,),
            )
            expected_holidays = [
                (
                    date(2024, 5, 1),
                    "The Labour Day",
                )
            ]
        self.assertEqual(holidays, expected_holidays)

    @patch(
        "server.employee_management.apps.employee_holidays.backends.pypi_holidays.country_holidays"
    )
    def test_get_upcoming_holidays(self, mock_country_holidays):
        mock_country_holidays.return_value = {
            date(2024, 5, 1): "The Labour Day",
            date(2024, 5, 6): "Sham El-Nassim",
            date(2024, 6, 30): "30 June Revolution",
        }
        with patch(
            "server.employee_management.apps.employee_holidays.backends.pypi_holidays.date"
        ) as mock_holidays:
            mock_holidays.today.return_value = date(2024, 4, 29)
            # This is already a monday, so the next_seven_days will end in datetime.date(2024, 5, 6)
            holidays = self.backend.get_upcoming_holidays(
                country=self.country,
                categories=(self.holiday_category,),
            )
            expected_holidays = [
                (
                    date(2024, 5, 1),
                    "The Labour Day",
                ),
                (
                    date(2024, 5, 6),
                    "Sham El-Nassim",
                ),
            ]
        self.assertEqual(holidays, expected_holidays)

    @patch(
        "server.employee_management.apps.employee_holidays.backends.pypi_holidays.country_holidays"
    )
    def test_get_upcoming_holidays_not_monday(self, mock_country_holidays):
        mock_country_holidays.return_value = {
            date(2024, 5, 1): "The Labour Day",
            date(2024, 5, 6): "Sham El-Nassim",
            date(2024, 6, 30): "30 June Revolution",
        }
        with patch(
            "server.employee_management.apps.employee_holidays.backends.pypi_holidays.date"
        ) as mock_holidays:
            mock_holidays.today.return_value = date(2024, 5, 1)
            holidays = self.backend.get_upcoming_holidays(
                country=self.country,
                categories=(self.holiday_category,),
            )
            expected_holidays = None
        self.assertEqual(holidays, expected_holidays)


if __name__ == "__main__":
    unittest.main()
