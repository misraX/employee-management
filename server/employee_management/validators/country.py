import pytz

from server.employee_management.exceptions.country import CountryValidationError
from server.employee_management.validators.validator import Validator


class CountryValidator(Validator):
    def __init__(self, value: str):
        self.value = value

    def validate(self):
        """
        Validate the country code.

        :return: self
        :raises CountryValidationError: If the country code is invalid.
        """
        country_code = self.value.upper()
        pytz_country_code = pytz.country_names.get(country_code)
        if not pytz_country_code:
            raise CountryValidationError("Invalid Country Code.")

        self.value = country_code
        return self
