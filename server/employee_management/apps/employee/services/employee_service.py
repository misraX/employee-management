import uuid
from datetime import date
from typing import Dict, List, Tuple

from holidays import PUBLIC

from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from server.employee_management.apps.employee_holidays.backends.backend import HolidaysBackend
from server.employee_management.apps.employee_holidays.backends.pypi_holidays import (
    PyPiHolidaysBackend,
)


class EmployeeService:
    def __init__(
        self,
        employee_repository: EmployeeSQLiteRepository = EmployeeSQLiteRepository,
        holidays_backend: HolidaysBackend = PyPiHolidaysBackend,
    ):
        self._employee_repository = employee_repository
        self._holidays_backend = holidays_backend

    def add_employee(self, employee: Employee) -> Employee:
        return self._employee_repository.add(employee)

    def get_employee(self, employee_id: uuid.UUID) -> Employee | None:
        return self._employee_repository.get(entity_id=employee_id)

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        return self._employee_repository.delete(entity_id=employee_id)

    def update_employee(self, employee_id: uuid.UUID, values: Dict) -> Employee:
        if not values:
            raise ValueError("Employee values cannot be empty")
        return self._employee_repository.update(entity_id=employee_id, update=values)

    def get_all_employees(self) -> List[Employee] | None:
        return self._employee_repository.get_all()

    def get_employee_current_holiday(
        self, employee_id: uuid.UUID, categories: Tuple[str] = (PUBLIC,)
    ) -> List[tuple[date, str]] | None:
        employee = self._employee_repository.get(entity_id=employee_id)
        if not employee or not employee.country:
            return None

        holidays = self._holidays_backend.get_current_week_holidays(
            country=employee.country, categories=categories
        )
        return holidays if holidays else None
