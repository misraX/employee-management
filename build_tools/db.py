from employee_management.core.configurations.configuration import configuration
from employee_management.database.sqlite_database_initializer import SQLiteDatabaseInitializer

if __name__ == "__main__":
    db_name = configuration.database_url
    db_initializer = SQLiteDatabaseInitializer(db_name=db_name)
    db_initializer.create_employee_table()
