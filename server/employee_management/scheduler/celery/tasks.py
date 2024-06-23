from celery.utils.log import get_task_logger
from holidays import PUBLIC

from server.employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from server.employee_management.apps.employee.services.employee_service import EmployeeService
from server.employee_management.apps.employee_holidays.backends.pypi_holidays import (
    PyPiHolidaysBackend,
)
from server.employee_management.core.configurations.configuration import configuration
from server.employee_management.notifications.notify_by_email import NotifyByEmail
from server.employee_management.scheduler.celery.celery_config import app

logger = get_task_logger(__name__)


@app.task
def employee_upcoming_holidays():
    employee_repository = EmployeeSQLiteRepository()
    holidays_backend = PyPiHolidaysBackend()

    employee_service = EmployeeService(
        employee_repository=employee_repository, holidays_backend=holidays_backend
    )
    offset = 0
    limit = 100
    while True:
        all_employees = employee_service.get_all_employees(offset=offset, limit=limit)
        if not all_employees:
            break
        for employee in all_employees:
            try:
                holidays = holidays_backend.get_upcoming_holidays(
                    country=employee.country, categories=(PUBLIC,)
                )
                if holidays:
                    message = "Your upcoming public holidays are as follows:"
                    for holiday in holidays:
                        message += f"\nDate: {holiday[0]} - Holiday: - {holiday[1]}"
                    email = NotifyByEmail(
                        message=message,
                        to_email=employee.email,
                        from_email=configuration.smtp_user,
                        subject="Upcoming Holidays",
                        smtp_server=configuration.smtp_server,
                        smtp_port=configuration.smtp_port,
                        smtp_user=configuration.smtp_user,
                        smtp_password=configuration.smtp_password,
                    )
                    email.send()  # Email exceptions already handled internally
            except Exception as e:
                logger.warning(f"Exception raised while getting upcoming holidays: {e}")
        offset += limit


@app.task
def dummy():
    logger.info("Dummy task executed.")
