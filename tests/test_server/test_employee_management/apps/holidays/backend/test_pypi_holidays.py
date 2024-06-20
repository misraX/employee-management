import unittest

from faker import Faker
from holidays import PUBLIC

from server.employee_management.apps.holidays.backends.pypi_holidays import PyPiHolidaysBackend

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


if __name__ == "__main__":
    unittest.main()
