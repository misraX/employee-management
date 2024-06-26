import os
import unittest
import uuid
from unittest.mock import patch

from faker import Faker

from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from server.employee_management.apps.employee.services.employee_service import EmployeeService
from server.employee_management.core.configurations.configuration import configuration
from server.employee_management.database.sqlite_database_initializer import (
    SQLiteDatabaseInitializer,
)
from server.employee_management.database.sqlite_database_session import SQLiteDatabaseSession
from server.employee_management.utilities.time import TimeUtility

config = configuration
faker = Faker()


class EmployeeServiceTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URL"] = "example.db"
        # Initialize the employee tables
        db_initializer = SQLiteDatabaseInitializer(db_name=config.database_url)
        db_initializer.create_employee_table()
        self.repository = EmployeeSQLiteRepository()
        self.db_session = SQLiteDatabaseSession()
        self.employee_name = faker.name()
        self.employee_email = faker.email()
        self.employee_salary = faker.pyfloat(min_value=100, max_value=2000)
        self.employee_service = EmployeeService(employee_repository=self.repository)

    def tearDown(self):
        db_path = config.database_url
        os.remove(db_path)

    def test_add_employee(self):
        employee_id = uuid.uuid4()
        employee = Employee(
            employee_id=employee_id,
            name=self.employee_name,
            position="Software Engineer",
            email=self.employee_email,
            salary=self.employee_salary,
            country="US",
        )
        now = "2024-06-20 00:03:42.746949+00:00"
        with patch.object(TimeUtility, "get_current_time", return_value=now):
            added_employee = self.employee_service.add_employee(employee=employee)

        self.assertEqual(added_employee, employee)
        self.db_session.open()
        cursor = self.db_session.get_cursor()
        cursor.execute("SELECT * FROM employee WHERE employee_id = ?", (str(employee_id),))
        result = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(result)
        self.assertEqual(result["employee_id"], str(employee_id))
        self.assertEqual(result["name"], self.employee_name)
        self.assertEqual(result["position"], "Software Engineer")
        self.assertEqual(result["email"], self.employee_email)
        self.assertEqual(result["salary"], self.employee_salary)
        self.assertEqual(result["created_at"], now)
        self.assertEqual(result["updated_at"], now)

    def test_update_employee(self):
        employee = Employee(
            name=self.employee_name,
            position="Software Engineer",
            email=self.employee_email,
            salary=self.employee_salary,
            country="US",
        )
        now = "2024-06-20 00:03:42.746949+00:00"
        with patch.object(TimeUtility, "get_current_time", return_value=now):
            added_employee = self.employee_service.add_employee(employee=employee)
        updated_employee = {"name": faker.name(), "position": "Software Engineer"}
        update = self.employee_service.update_employee(
            employee_id=employee.employee_id, values=updated_employee
        )
        self.assertEqual(
            str(employee.employee_id), update.employee_id
        )  # Runtime won't convert the type
        self.assertNotEqual(added_employee.name, updated_employee.get("name"))

    def test_delete_employee(self):
        employee = Employee(
            name=self.employee_name,
            position="Software Developer",
            email=self.employee_email,
            salary=self.employee_salary,
            country="US",
        )
        self.employee_service.add_employee(employee=employee)

        self.employee_service.delete_employee(employee_id=employee.employee_id)
        deleted_employee = self.employee_service.get_employee(employee_id=employee.employee_id)
        self.assertIsNone(deleted_employee)

    def test_list_employees(self):
        seeds = [
            Employee(
                name=faker.name(),
                position="Software Developer",
                email=faker.email(),
                salary=faker.pyfloat(min_value=100, max_value=2000),
                country=faker.country_code(),
                employee_id=uuid.uuid4(),
            )
            for _ in range(1000)
        ]

        for seed in seeds:
            now = "2024-06-20 00:03:42.746949+00:00"
            with patch.object(TimeUtility, "get_current_time", return_value=now):
                self.employee_service.add_employee(employee=seed)
        offset = 0
        limit = 100
        counter = 0
        list_only_one_employee = self.employee_service.get_all_employees(offset=offset, limit=1)
        self.assertEqual(len(list_only_one_employee), 1)
        while True:
            list_of_employees = self.employee_service.get_all_employees(offset=offset, limit=limit)
            if not list_of_employees:
                break
            counter += list_of_employees.__len__()
            offset += limit

        self.assertEqual(counter, seeds.__len__())


if __name__ == "__main__":
    unittest.main()
