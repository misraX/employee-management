from email_validator import validate_email

from employee_management_system.exceptions.email import EmailValidationException


class EmailValidator:
    @staticmethod
    def email(email):
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except Exception as exception:
            raise EmailValidationException(exception) from exception
        return email
