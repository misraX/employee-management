import os

from employee_management_system.core.configurations.configuration import configuration
from employee_management_system.database.sqlite_database_initializer import (
    SQLiteDatabaseInitializer,
)
from employee_management_system.logging.logger import format_logger_name
from employee_management_system.logging.logger import logger as logging

logger = logging.getLogger(format_logger_name(configuration.app_name))


def main():
    config = configuration
    os.environ["DATABASE_URL"] = "example.db"
    db_initializer = SQLiteDatabaseInitializer(db_name=config.database_url)
    db_initializer.create_employee_table()


if __name__ == "__main__":
    main()
