import unittest
from unittest import TestCase

from faker import Faker

from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.exceptions.email import EmailValidationException
from server.employee_management.exceptions.immutable import ImmutableAttributeError
from server.employee_management.utilities.time import TimeUtility

faker = Faker()


class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.current_time = TimeUtility.get_current_time()
        self.employee_name = faker.name()
        self.employee_email = faker.email()
        self.employee_salary = faker.pyfloat(min_value=100, max_value=2000)
        self.employee_invalid_email = "invalid-email"
        self.employee = Employee(
            name=self.employee_name,
            email=self.employee_email,
            salary=self.employee_salary,
            created_at=self.current_time,
            updated_at=self.current_time,
            position="Software Developer",
        )

    def test_employee(self):
        self.assertEqual(self.employee.name, self.employee_name)
        self.assertEqual(self.employee.email, self.employee_email)
        self.assertEqual(self.employee.salary, self.employee_salary)
        self.assertEqual(self.employee.created_at, self.current_time)
        self.assertEqual(self.employee.updated_at, self.current_time)

    def test_employee_invalid_email(self):
        with self.assertRaises(EmailValidationException) as exception:
            Employee(
                name=self.employee_name,
                email=self.employee_invalid_email,
                salary=self.employee_salary,
                created_at=self.current_time,
                updated_at=self.current_time,
                position="Software Developer",
            )

        self.assertEqual(
            str(exception.exception),
            "An email address must have an @-sign.",
        )

    def test_immutable_employee_name(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.name = faker.name()

        self.assertEqual(str(exception.exception), "Cannot modify the name attribute.")

    def test_immutable_employee_email(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.email = faker.email()

        self.assertEqual(str(exception.exception), "Cannot modify the email attribute.")

    def test_immutable_employee_salary(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.salary = faker.pyfloat(min_value=100, max_value=2000)

        self.assertEqual(str(exception.exception), "Cannot modify the salary attribute.")

    def test_immutable_employee_position(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.position = faker.word()

        self.assertEqual(str(exception.exception), "Cannot modify the position attribute.")

    def test_immutable_employee_created_at(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.created_at = TimeUtility.get_current_time()
        self.assertEqual(str(exception.exception), "Cannot modify the created_at attribute.")

    def test_immutable_employee_updated_at(self):
        with self.assertRaises(ImmutableAttributeError) as exception:
            self.employee.updated_at = TimeUtility.get_current_time()

        self.assertEqual(str(exception.exception), "Cannot modify the updated_at attribute.")


if __name__ == "__main__":
    unittest.main()
