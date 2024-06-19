from datetime import datetime
from typing import Final

from employee_management.validators.email import EmailValidator


class Employee:
    """
    A model representing an employee, this object ensure that the properties are final and immutable.

    By using python's setters we ensure the immutability of the object properties.
    """

    def __init__(
        self,
        name: str,
        salary: float,
        position: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self._name: Final[str] = name
        self._salary: Final[float] = salary
        self._position: Final[str] = position
        self._email: Final[str] = EmailValidator.email(email)
        self._created_at: Final[datetime] = created_at
        self._updated_at: Final[datetime] = updated_at

    def __str__(self):
        return f"Employee {self.name} - salary {self.salary} - position {self.position} - email {self.email} - created at {self.created_at} - updated at {self.updated_at} "

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        raise AttributeError("Cannot modify the name attribute.")

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, salary: float):
        raise AttributeError("Cannot modify salary attribute.")

    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, position: str):
        raise AttributeError("Cannot modify position attribute.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        raise AttributeError("Cannot modify email attribute.")

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        raise AttributeError("Cannot modify created_at attribute.")

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        raise AttributeError("Cannot modify updated_at attribute.")
