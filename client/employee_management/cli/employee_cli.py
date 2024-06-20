import uuid
from typing import Dict, List

from client.employee_management.models.employee_model import EmployeeModel
from employee_management.apps.employee.models.employee import Employee
from employee_management.apps.employee.services.employee_service import EmployeeService


class EmployeeCLI:
    """
    A CLI object to manage employee management.
    The CLI uses the employee service to manage the employee operations.

    It's simply a wrapper around the EmployeeService class, which easily
    interacts with the EmployeeService class.
    """

    def __init__(self, service: EmployeeService, utils: EmployeeModel):
        self.service = service
        self.utils = utils

    def add_employee(self, name: str, salary: float, position: str, email: str) -> Dict[str, str]:
        """Create and add a new employee."""
        employee = Employee(name=name, salary=salary, position=position, email=email)
        added_employee = self.service.add_employee(employee=employee)
        return self.utils.employee_to_dict(added_employee)

    def get_employee(self, employee_id: str) -> Dict[str, str]:
        """Retrieve an employee by ID."""
        employee_id = uuid.UUID(employee_id)
        employee = self.service.get_employee(employee_id=employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return self.utils.employee_to_dict(employee=employee)

    def delete_employee(self, employee_id: str) -> None:
        """Delete an employee by ID."""
        self.service.delete_employee(uuid.UUID(employee_id))

    def update_employee(self, employee_id: str, updates: Dict[str, str]) -> Dict[str, str]:
        """Update an existing employee."""
        employee = self.service.get_employee(uuid.UUID(employee_id))
        if not employee:
            raise ValueError("Employee not found")
        updated_employee = Employee(
            name=updates.get("name", employee.name),
            salary=updates.get("salary", employee.salary),
            position=updates.get("position", employee.position),
            email=updates.get("email", employee.email),
            employee_id=uuid.UUID(employee_id),
        )
        update_values = self.utils.employee_to_dict(employee=updated_employee, read=False)
        self.service.update_employee(employee_id=uuid.UUID(employee_id), values=update_values)
        return self.utils.employee_to_dict(updated_employee)

    def list_employees(self) -> List[Dict[str, str]]:
        """List all employees."""
        employees = self.service.get_all_employees()
        return [self.utils.employee_to_dict(employee=employee) for employee in employees]
