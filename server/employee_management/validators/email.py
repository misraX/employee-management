from email_validator import validate_email

from server.employee_management.exceptions.email import EmailValidationException


class EmailValidator:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def validate(self) -> "EmailValidator":
        try:
            email_info = validate_email(self.value, check_deliverability=False)
            self.value = email_info.normalized
        except Exception as exception:
            raise EmailValidationException(exception) from exception
        return self
