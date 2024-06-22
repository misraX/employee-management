import datetime
import unittest
import uuid
from unittest.mock import Mock

from faker import Faker

from client.employee_management.cli.employee_cli import EmployeeCLI
from client.employee_management.models.employee_model import EmployeeModel
from client.employee_management.models.holidays_model import HolidaysModel
from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.apps.employee.services.employee_service import EmployeeService

faker = Faker()


class EmployeeCLITestCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock(spec=EmployeeService)
        self.mock_employee_model = Mock(spec=EmployeeModel)
        self.mock_holidays_model = Mock(spec=HolidaysModel)

        self.cli = EmployeeCLI(
            service=self.mock_service,
            employee_model=self.mock_employee_model,
            holidays_model=self.mock_holidays_model,
        )
        name = faker.name()
        salary = faker.pyint(min_value=100, max_value=2000)
        email = faker.email()
        country = faker.country_code()
        position = "Software Engineer"
        self.test_employee = Employee(
            name=name, salary=salary, email=email, country=country, position=position
        )
        self.test_employee_dict = {
            "name": name,
            "salary": salary,
            "email": email,
            "country": country,
            "employee_id": self.test_employee.employee_id,
        }

    def test_add_employee(self):
        test_employee = Mock()
        name = faker.name()
        salary = faker.pyint(min_value=100, max_value=2000)
        email = faker.email()
        country = faker.country_code()
        position = "Software Engineer"
        test_employee_dict = {"name": name, "salary": salary, "email": email, "country": country}
        self.mock_employee_model.to_dict.return_value = test_employee_dict
        self.mock_service.add_employee.return_value = test_employee
        result = self.cli.add_employee(
            name=name, salary=salary, email=email, country=country, position=position
        )
        self.mock_service.add_employee.assert_called_once()
        self.mock_employee_model.to_dict.assert_called_once_with(test_employee)
        self.assertEqual(result, test_employee_dict)

    def test_get_employee_not_found(self):
        self.mock_service.get_employee.return_value = None

        with self.assertRaises(ValueError) as context:
            self.cli.get_employee("123e4567-e89b-12d3-a456-426614174000")
        self.assertTrue("Employee not found" in str(context.exception))

    def test_update_employee_not_found(self):
        self.mock_service.get_employee.return_value = None
        updates = {"name": faker.name(), "salary": faker.pyfloat(min_value=100, max_value=2000)}

        with self.assertRaises(ValueError) as context:
            self.cli.update_employee("123e4567-e89b-12d3-a456-426614174000", updates)
        self.assertTrue("Employee not found" in str(context.exception))

    def test_update_employee(self):
        self.mock_employee_model.to_dict.return_value = self.test_employee_dict
        self.mock_service.add_employee.return_value = self.test_employee
        result = self.cli.add_employee(
            name=self.test_employee.name,
            salary=self.test_employee.salary,
            email=self.test_employee.email,
            country=self.test_employee.country,
            position=self.test_employee.position,
        )
        self.mock_service.add_employee.assert_called_once()
        self.mock_employee_model.to_dict.assert_called_once_with(self.test_employee)
        self.assertEqual(result, self.test_employee_dict)
        self.mock_service.get_employee.return_value = self.test_employee
        updates = {"name": faker.name(), "salary": faker.pyfloat(min_value=100, max_value=2000)}
        updates_employee_dict = {"name": faker.name()}
        self.test_employee_dict.update(updates)
        self.mock_employee_model.to_dict.return_value = updates_employee_dict
        update_employee = self.cli.update_employee(f"{self.test_employee.employee_id}", updates)
        self.assertEqual(updates_employee_dict.get("name"), update_employee.get("name"))
        self.assertNotEqual(updates_employee_dict.get("name"), self.test_employee_dict.get("name"))
        self.mock_employee_model.to_dict.call_counts = 3  # get, update -> <get>

    def test_list_employees(self):
        employees = [self.test_employee]
        self.mock_service.get_all_employees.return_value = employees
        self.mock_employee_model.to_dict.return_value = self.test_employee_dict

        result = self.cli.list_employees()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_employee_dict)
        self.mock_service.get_all_employees.assert_called_once()
        self.mock_employee_model.to_dict.assert_called_once_with(employee=employees[0])

    def test_list_employees_empty(self):
        self.mock_service.get_all_employees.return_value = []

        result = self.cli.list_employees()

        self.assertEqual(len(result), 0)
        self.mock_service.get_all_employees.assert_called_once()
        self.mock_employee_model.to_dict.call_counts = 0

    def test_get_employee_current_holiday_found(self):
        employee_id = uuid.uuid4()
        holiday_data = [(datetime.date(2024, 12, 22), "Christmas Day")]
        formatted_holidays = [{"date": "2024-12-25", "name": "Christmas Day"}]

        self.mock_service.get_employee_current_holiday.return_value = holiday_data
        self.mock_holidays_model.to_dict.side_effect = lambda holidays: formatted_holidays

        result = self.cli.get_employee_current_holiday(str(employee_id))

        self.mock_service.get_employee_current_holiday.assert_called_once_with(employee_id)
        self.assertEqual(result, formatted_holidays)

    def test_get_employee_current_holiday_none_found(self):
        employee_id = uuid.uuid4()
        self.mock_service.get_employee_current_holiday.return_value = []

        result = self.cli.get_employee_current_holiday(str(employee_id))

        self.mock_service.get_employee_current_holiday.assert_called_once_with(employee_id)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
