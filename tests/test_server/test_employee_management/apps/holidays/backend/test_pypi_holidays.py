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

        backend = PyPiHolidaysBackend()

        holidays = backend.get_holidays(
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

        backend = PyPiHolidaysBackend()

        holidays = backend.get_holidays(
            country="US", years=[2024], categories=("public",), language="en_US"
        )

        expected_holidays = [
            (date(2024, 1, 1), "New Year's Day"),
            (date(2024, 12, 25), "Christmas Day"),
        ]

        self.assertEqual(holidays, expected_holidays)


if __name__ == "__main__":
    unittest.main()
