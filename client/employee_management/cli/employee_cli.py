import uuid
from datetime import date
from typing import Dict, List

from client.employee_management.models.employee_model import EmployeeModel
from client.employee_management.models.holidays_model import HolidaysModel
from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.apps.employee.services.employee_service import EmployeeService


class EmployeeCLI:
    """
    A CLI object to manage employee management.
    The CLI uses the employee service to manage the employee operations.

    It's simply a wrapper around the EmployeeService class, which easily
    interacts with the EmployeeService class.
    """

    def __init__(
        self, service: EmployeeService, employee_model: EmployeeModel, holidays_model: HolidaysModel
    ):
        self.service = service
        self.employee_model = employee_model
        self.holidays_model = holidays_model

    def add_employee(
        self, name: str, salary: float, position: str, email: str, country: str
    ) -> Dict[str, str]:
        """
        Create and add a new employee.

        :param name: The name of the employee.
        :param salary: The salary of the employee.
        :param position: The position of the employee.
        :param email: The email of the employee.
        :param country: The country of the employee.
        :return: The created employee.
        """
        employee = Employee(
            name=name, salary=salary, position=position, email=email, country=country
        )
        added_employee = self.service.add_employee(employee=employee)
        return self.employee_model.to_dict(added_employee)

    def get_employee(self, employee_id: str) -> Dict[str, str]:
        """
        Retrieve an employee by ID.

        :param employee_id: ID of the employee.
        """
        employee_id = uuid.UUID(employee_id)
        employee = self.service.get_employee(employee_id=employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return self.employee_model.to_dict(employee=employee)

    def delete_employee(self, employee_id: str) -> None:
        """
        Delete an employee by ID.

        :param employee_id: ID of the employee to delete.
        """
        self.service.delete_employee(uuid.UUID(employee_id))

    def update_employee(self, employee_id: str, updates: Dict[str, str]) -> Dict[str, str]:
        """
        Update an existing employee.

        :param employee_id: ID of the employee to update.
        :param updates: Dictionary of updates to apply to the employee.
        :return: Dictionary of updated employee.
        """
        employee = self.service.get_employee(uuid.UUID(employee_id))
        if not employee:
            raise ValueError("Employee not found")
        updated_employee = Employee(
            name=updates.get("name", employee.name),
            salary=updates.get("salary", employee.salary),
            position=updates.get("position", employee.position),
            email=updates.get("email", employee.email),
            country=updates.get("country", employee.country),
            employee_id=uuid.UUID(employee_id),
        )
        update_values = self.employee_model.to_dict(employee=updated_employee, read=False)
        self.service.update_employee(employee_id=uuid.UUID(employee_id), values=update_values)
        return self.employee_model.to_dict(updated_employee)

    def list_employees(self) -> List[Dict[str, str]]:
        """
        List all employees.

        :return: List of employees.
        """
        employees = self.service.get_all_employees()
        return [self.employee_model.to_dict(employee=employee) for employee in employees]

    def get_employee_current_holiday(self, employee_id: str) -> list[tuple[date, str]] | None:
        """
        Get current holiday for an employee.

        :param employee_id: employee ID
        :return: list of holidays or None
        """
        holidays = self.service.get_employee_current_holiday(uuid.UUID(employee_id))
        return self.holidays_model.to_dict(holidays=holidays)
