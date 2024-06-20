import uuid
from datetime import datetime
from typing import Final

from server.employee_management.exceptions.immutable import ImmutableAttributeError
from server.employee_management.utilities.time import TimeUtility
from server.employee_management.validators.email import EmailValidator


class Employee:
    """
    A model representing an employee, this object ensure that the properties
    are final and immutable.

    By using python's setters we ensure the immutability of the object properties.
    """

    def __init__(
        self,
        name: str,
        salary: float,
        position: str,
        email: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        employee_id: uuid.UUID | None = None,
        country: str | None = None,
    ):
        self._name: Final[str] = name
        self._salary: Final[float] = salary
        self._position: Final[str] = position
        self._email: Final[str] = EmailValidator.email(email)
        self._created_at: Final[datetime] = (
            created_at if created_at else TimeUtility.get_current_time()
        )
        self._updated_at: Final[datetime] = (
            updated_at if updated_at else TimeUtility.get_current_time()
        )
        self._employee_id: Final[uuid.UUID] = employee_id if employee_id else uuid.uuid4()
        self._country: Final[str] = country

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        raise ImmutableAttributeError("Cannot modify the name attribute.")

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, salary: float):
        raise ImmutableAttributeError("Cannot modify the salary attribute.")

    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, position: str):
        raise ImmutableAttributeError("Cannot modify the position attribute.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        raise ImmutableAttributeError("Cannot modify the email attribute.")

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        raise ImmutableAttributeError("Cannot modify the created_at attribute.")

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        raise ImmutableAttributeError("Cannot modify the updated_at attribute.")

    @property
    def employee_id(self) -> uuid.UUID:
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id: uuid.UUID):
        raise ImmutableAttributeError("Cannot modify the employee id")

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        raise ImmutableAttributeError("Cannot modify the country attribute.")

    def __str__(self):
        return (
            f"Employee: <{self.employee_id}> {self.name} - salary {self.salary} "
            f"- position {self.position} - email {self.email} - created at {self.created_at}"
            f"- updated at {self.updated_at}"
        )
