import uuid

from employee_management_system.apps.employee.models.employee import Employee
from employee_management_system.core.repositories.base_repository import CRUDRepository
from employee_management_system.database.sqlite_database_session import SQLiteDatabaseSession


class EmployeeRepository(CRUDRepository[Employee]):
    def __init__(self):
        self.db_session = SQLiteDatabaseSession()

    def get(self, entity_id: uuid.UUID) -> Employee:
        pass

    def delete(self, entity_id: uuid.UUID) -> None:
        pass

    def add(self, entity: Employee) -> Employee:
        pass

    def update(self, entity_id: uuid.UUID, update: Employee) -> Employee:
        pass
