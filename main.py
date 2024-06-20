import json

import click

from client.cli.employee_management.employee_cli import EmployeeCLI
from client.cli.employee_management.employee_utils import EmployeeUtils
from client.cli.employee_management.timezone_utils import TimezoneUtils
from employee_management.apps.employee.repositories.employee_repository import (
    EmployeeSQLiteRepository,
)
from employee_management.apps.employee.services.employee_service import EmployeeService

timezone_utils = TimezoneUtils()
employee_utils = EmployeeUtils(timezone_utils)
employee_repository = EmployeeSQLiteRepository()
employee_service = EmployeeService(employee_repository=employee_repository)
employee_cli = EmployeeCLI(employee_service, employee_utils)


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
    added_employee = employee_cli.add_employee(name, salary, position, email)
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
def list():
    """List all employees 📋"""
    employees = employee_cli.list_employees()
    click.echo("📋 List of employees:")
    click.echo(json.dumps(employees, indent=4))


if __name__ == "__main__":
    cli()
