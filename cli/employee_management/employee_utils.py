from typing import Dict

from cli.employee_management.timezone_utils import TimezoneUtils
from employee_management.apps.employee.models.employee import Employee


class EmployeeUtils:
    """
    A utility class to manage employee, it's used to serialize the employee
    based on read/write operations.
    """

    def __init__(self, timezone_utils: TimezoneUtils):
        self.timezone_utils = timezone_utils

    def employee_to_dict(self, employee: Employee, read: bool = True) -> Dict[str, str]:
        """
        Convert an Employee object to a dictionary.

        :param Employee employee: Employee object to convert.
        :param bool read: Read Employee object to convert.
        :return: Dictionary of employee.
        """
        employee_dict = dict()
        employee_dict.update(
            {
                "name": employee.name,
                "salary": employee.salary,
                "position": employee.position,
                "email": employee.email,
            }
        )
        if read:
            employee_dict.update(
                {
                    "employee_id": str(employee.employee_id),
                    "created_at": self.timezone_utils.to_local_timezone(str(employee.created_at)),
                    "updated_at": self.timezone_utils.to_local_timezone(str(employee.updated_at)),
                }
            )

        return employee_dict
