class EmailValidationException(ValueError):
    """
    Exception raised when an invalid email address is passed, proxying email_validator.validate_email exceptions
    """

    ...
