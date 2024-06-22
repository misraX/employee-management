import json

import click

from client.employee_management.cli.employee_cli import EmployeeCLI
from client.employee_management.models.employee_model import EmployeeModel
from client.employee_management.models.holidays_model import HolidaysModel
from client.employee_management.utilities.timezone_utils import TimezoneUtils
from server.employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from server.employee_management.apps.employee.services.employee_service import EmployeeService
from server.employee_management.apps.employee_holidays.backends.pypi_holidays import (
    PyPiHolidaysBackend,
)

timezone_utils = TimezoneUtils()
employee_model = EmployeeModel(timezone_utils=timezone_utils)
holiday_model = HolidaysModel()
employee_repository = EmployeeSQLiteRepository()
holidays_backend = PyPiHolidaysBackend()
employee_service = EmployeeService(
    employee_repository=employee_repository, holidays_backend=holidays_backend
)
employee_cli = EmployeeCLI(
    service=employee_service, employee_model=employee_model, holidays_model=holiday_model
)


@click.group()
def cli():
    """✨ Employee Management CLI ✨"""
    pass


@cli.command()
def add():
    """Add a new employee ✨"""
    name = click.prompt("Please enter the employee name")
    salary = click.prompt("Please enter the employee salary", type=float)
    position = click.prompt("Please enter the employee position")
    email = click.prompt("Please enter the employee email")
    country = click.prompt("Please enter the employee country code")
    added_employee = employee_cli.add_employee(
        name=name, salary=salary, position=position, email=email, country=country
    )
    click.echo("✨ Employee added successfully! ✨")
    click.echo(json.dumps(added_employee, indent=4))


@cli.command()
@click.argument("employee_id")
def get(employee_id):
    """Get an employee by ID 🔍"""
    try:
        employee = employee_cli.get_employee(employee_id)
        click.echo("🔍 Employee found:")
        click.echo(json.dumps(employee, indent=4))
    except ValueError:
        click.echo("❌ Employee not found ❌")


@cli.command()
@click.argument("employee_id")
def delete(employee_id):
    """Delete an employee by ID 🗑️"""
    try:
        employee_cli.delete_employee(employee_id)
        click.echo("🗑️ Employee deleted 🗑️")
    except ValueError:
        click.echo("❌ Employee not found ❌")


@cli.command()
@click.argument("employee_id")
def update(employee_id):
    """Update an existing employee ✨"""
    updates = {}
    if click.confirm("Do you want to update the name?"):
        updates["name"] = click.prompt("Please enter the new name", type=str)
    if click.confirm("Do you want to update the salary?"):
        updates["salary"] = click.prompt("Please enter the new salary", type=float)
    if click.confirm("Do you want to update the position?"):
        updates["position"] = click.prompt("Please enter the new position", type=str)
    if click.confirm("Do you want to update the email?"):
        updates["email"] = click.prompt("Please enter the new email", type=str)
    if click.confirm("Do you want to update the country?"):
        updates["country"] = click.prompt("Please enter the new country", type=str)

    if not updates.keys():
        click.echo("🚫 Oops! Nothing to update!")
        return
    try:
        updated_employee = employee_cli.update_employee(employee_id=employee_id, updates=updates)
        click.echo("✨ Employee updated successfully! ✨")
        click.echo(json.dumps(updated_employee, indent=4))
    except ValueError as exc:
        click.echo(f"❌ {exc.__str__()} ❌")


@cli.command()
@click.argument("employee_id")
def get_current_employee_holiday(employee_id):
    """Get the current week public holidays 🍹"""
    holidays = employee_cli.get_employee_current_holiday(employee_id=employee_id)
    click.echo("🍹 List of employee's current week holidays")
    click.echo(json.dumps(holidays, indent=4))


@cli.command()
def list():
    """List all employees 📋"""
    offset = 0
    limit = 1000
    counter = 0
    while True:
        employees = employee_cli.list_employees(offset=offset, limit=limit)
        if not employees:
            break
        click.echo(json.dumps(employees, indent=4))
        employees_length = len(employees)
        counter += employees_length
        input(
            f"Press enter to continue <enter>, "
            f"current offset {offset}, "
            f"current count {counter}, "
            f"fetched employees {employees_length}."
        )
        offset += limit

    click.echo(f"Found {counter} employees!")


if __name__ == "__main__":
    cli()
