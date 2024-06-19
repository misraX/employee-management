from employee_management_system.core.configurations.configuration import configuration
from employee_management_system.database.database_initializer import DatabaseInitializer
from employee_management_system.logging.logger import format_logger_name
from employee_management_system.logging.logger import logger as logging

logger = logging.getLogger(format_logger_name(configuration.app_name))


def main():
    config = configuration
    db_initializer = DatabaseInitializer(db_name=config.database_url)
    db_initializer.create_employee_table()


if __name__ == "__main__":
    main()
