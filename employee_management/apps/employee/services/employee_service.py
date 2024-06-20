import uuid

from employee_management.apps.employee.models.employee import Employee
from employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)


class EmployeeService:
    def __init__(self, employee_repository: EmployeeSQLiteRepository = EmployeeSQLiteRepository):
        self._employee_repository = employee_repository

    def add_employee(self, employee: Employee) -> Employee:
        return self._employee_repository.add(employee)

    def get_employee(self, employee_id: uuid.UUID) -> Employee | None:
        return self._employee_repository.get(entity_id=employee_id)

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        return self._employee_repository.delete(entity_id=employee_id)

    def update_employee(self, employee_id: uuid.UUID, values: dict) -> Employee:
        if not values:
            raise ValueError("Employee values cannot be empty")
        return self._employee_repository.update(entity_id=employee_id, update=values)

    def get_all_employees(self) -> list[Employee] | None:
        return self._employee_repository.get_all()
