from unittest import TestCase

from faker import Faker

from employee_management.employee.models.employee import Employee
from employee_management.exceptions.email import EmailValidationException
from employee_management.utilities.time import TimeUtility

fake = Faker()


class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.current_time = TimeUtility.get_current_time()
        self.employee_name = fake.name()
        self.employee_email = fake.email()
        self.employee_salary = fake.pyfloat(min_value=100, max_value=2000)
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
            "The email address is not valid. It must have exactly one @-sign.",
        )

    def test_immutable_employee(self):
        with self.assertRaises(AttributeError) as exception:
            self.employee = Employee(
                name=self.employee_name,
                email=self.employee_email,
                salary=self.employee_salary,
                created_at=self.current_time,
                updated_at=self.current_time,
                position="Software Developer",
            )
            self.employee.name = fake.name()
            self.employee.email = fake.email()
            self.employee.salary = fake.pyfloat(min_value=100, max_value=2000)
            self.employee.created_at = self.current_time
            self.employee.updated_at = self.current_time
            self.employee.position = "Software Developer"
