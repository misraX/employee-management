import uuid

from server.employee_management.apps.employee.models.employee import Employee
from server.employee_management.core.repositories.base_repository import CRUDRepository, T
from server.employee_management.database.sqlite_database_session import SQLiteDatabaseSession
from server.employee_management.utilities.time import TimeUtility


class EmployeeSQLiteRepository(CRUDRepository[Employee]):
    def __init__(self):
        self._db_session = SQLiteDatabaseSession()

    def get(self, entity_id: uuid.UUID) -> Employee | None:
        """
        Get employee by id

        :param entity_id: employee id
        :return: Employee or None
        """
        with self._db_session as session:
            cursor = session.get_cursor()
            cursor.execute("SELECT * FROM employee WHERE employee_id = ?", (str(entity_id),))
            result = cursor.fetchone()
        return Employee(**result) if result is not None else None

    def delete(self, entity_id: uuid.UUID) -> None:
        """
        Delete an employee by entity_id

        :param entity_id: employee id
        :return: None
        """
        with self._db_session as db_session:
            cursor = db_session.get_cursor()
            cursor.execute("DELETE FROM employee WHERE employee_id = ?", (str(entity_id),))
            db_session.commit()

    def add(self, entity: Employee) -> Employee:
        """
        Adding an employee to the database

        :param entity: Employee
        :return: Employee
        """
        now = TimeUtility.get_current_time()
        with self._db_session as session:
            cursor = session.get_cursor()
            cursor.execute(
                """
                  INSERT INTO employee (
                  employee_id, name, position, email, salary, created_at, updated_at
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?)
              """,
                (
                    str(entity.employee_id),
                    entity.name,
                    entity.position,
                    entity.email,
                    entity.salary,
                    str(now),
                    str(now),
                ),
            )
            self._db_session.commit()
        return entity

    def update(self, entity_id: uuid.UUID, update: dict) -> Employee:
        columns = ", ".join(f"{key} = ?" for key in update)
        values = list(update.values())
        values.append(str(TimeUtility.get_current_time()))
        values.append(str(entity_id))
        with self._db_session as session:
            cursor = session.get_cursor()
            cursor.execute(
                f"""
                    UPDATE employee
                    SET {columns}, updated_at = ?
                    WHERE employee_id = ?
                """,
                values,
            )
            employee = cursor.execute(
                "SELECT * FROM employee WHERE employee_id = ?", (str(entity_id),)
            )
            result = employee.fetchone()
        employee = Employee(**result)
        return employee

    def get_all(self) -> list[T] | None:
        with self._db_session as session:
            cursor = session.get_cursor()
            cursor.execute("SELECT * FROM employee")
            result = cursor.fetchall()
        return [Employee(**result) for result in result] if result is not None else None

    def __str__(self):
        employees = self.get_all()
        if not employees:
            return ""
        items = []
        for employee in employees:
            items.append(employee.__str__())
        return f"{items}"
