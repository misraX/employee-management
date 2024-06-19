from employee_management_system.core.configurations.configuration import configuration
from employee_management_system.database.database_initializer import DatabaseInitializer


def main():
    # Initialize the database and create tables
    config = configuration
    db_initializer = DatabaseInitializer(db_name=config.database_url)
    db_initializer.create_employee_table()


if __name__ == "__main__":
    main()
