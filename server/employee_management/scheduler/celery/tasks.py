from server.employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from server.employee_management.apps.employee.services.employee_service import EmployeeService
from server.employee_management.apps.employee_holidays.backends.backend import HolidaysBackend
from server.employee_management.core.configurations.configuration import configuration
from server.employee_management.notifications.notify_by_email import NotifyByEmail
from server.employee_management.scheduler.celery.celery_config import app

employee_repository = EmployeeSQLiteRepository()
holidays_backend = HolidaysBackend()

employee_service = EmployeeService(
    employee_repository=employee_repository, holidays_backend=holidays_backend
)


@app.task
def employee_upcoming_holidays():
    all_employees = employee_service.get_all_employees()
    if all_employees:
        for employee in all_employees:
            if employee.country:
                email = NotifyByEmail(
                    message="Your upcoming public holidays are as follows",
                    to_email=employee.email,
                    from_email=configuration.smtp_user,
                    subject="Upcoming Holidays",
                    smtp_server=configuration.smtp_server,
                    smtp_port=configuration.smtp_port,
                    smtp_user=configuration.smtp_user,
                    smtp_password=configuration.smtp_password,
                )
                email.send()
