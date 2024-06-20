import uuid

from employee_management.apps.employee.models.employee import Employee
from employee_management.core.repositories.base_repository import CRUDRepository
from employee_management.database.sqlite_database_session import SQLiteDatabaseSession
from employee_management.utilities.time import TimeUtility


class EmployeeSQLiteRepository(CRUDRepository[Employee]):
    def __init__(self):
        self._db_session = SQLiteDatabaseSession()

    def get(self, entity_id: uuid.UUID) -> Employee:
        pass

    def delete(self, entity_id: uuid.UUID) -> None:
        pass

    def add(self, entity: Employee) -> Employee:
        """
        Adding an employee to the database

        :param entity: Employee
        :return: Employee
        """
        now = TimeUtility.get_current_time()
        self._db_session.open()
        cursor = self._db_session.get_cursor()
        cursor.execute(
            """
              INSERT INTO employee (
              employee_id, name, position, email, salary, created_at, updated_at
              )
              VALUES (?, ?, ?, ?, ?, ?, ?)
          """,
            (
                str(entity.entity_id),
                entity.name,
                entity.position,
                entity.email,
                entity.salary,
                str(now),
                str(now),
            ),
        )
        self._db_session.commit()
        cursor.close()
        return entity

    def update(self, entity_id: uuid.UUID, update: Employee) -> Employee:
        pass
