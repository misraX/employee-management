import sqlite3

from employee_management_system.core.configurations.configuration import configuration
from employee_management_system.core.database.sql_session import SQLSession
from employee_management_system.exceptions.sqlite_database import (
    DatabaseConnectionError,
    DatabaseOperationError,
)
from employee_management_system.logging.logger import format_logger_name
from employee_management_system.logging.logger import logger as logging

logger = logging.getLogger(format_logger_name("sqlite_database_session"))


class SQLiteDatabaseSession(SQLSession):
    def __init__(self):
        self._db_name: str = configuration.database_url
        self._connection: sqlite3.Connection | None = None
        self._cursor: sqlite3.Cursor | None = None

    def open(self) -> None:
        """
        Open a database session

        :return: None
        """
        try:
            self._connection = sqlite3.connect(self._db_name)
            self._connection.row_factory = sqlite3.Row
            self._cursor = self._connection.cursor()
            logger.info(f"Database connection opened: {self._db_name}")
        except sqlite3.Error as e:
            logger.error(f"Error opening database connection: {e}")
            raise DatabaseConnectionError(f"Failed to open database connection: {e}") from e

    def close(self) -> None:
        """
        Close the database session
        :return: None
        """
        try:
            if self._cursor:
                self._cursor.close()
                logger.info("Database cursor closed")
        except sqlite3.Error as e:
            logger.error(f"Error closing cursor: {e}")
            raise DatabaseOperationError(f"Failed to close cursor: {e}") from e
        try:
            if self._connection:
                self._connection.close()
                logger.info("Database connection closed")
        except sqlite3.Error as e:
            logger.error(f"Error closing connection: {e}")
            raise DatabaseOperationError(f"Failed to close connection: {e}") from e

    def commit(self) -> None:
        """
        Commit changes to the database
        :return: None
        """
        if not self._connection:
            raise DatabaseConnectionError("Database session is not open. Call 'open' first.")
        try:
            self._connection.commit()
            logger.info("Database changes committed")
        except sqlite3.Error as e:
            logger.error(f"Error committing changes: {e}")
            raise DatabaseOperationError(f"Failed to commit changes: {e}") from e

    def rollback(self) -> None:
        """
        Rollback changes to the database
        :return: None
        """
        if not self._connection:
            raise DatabaseConnectionError("Database session is not open. Call 'open' first.")
        try:
            self._connection.rollback()
            logger.info("Database changes rolled back")
        except sqlite3.Error as e:
            logger.error(f"Error rolling back changes: {e}")
            raise DatabaseOperationError(f"Failed to rollback changes: {e}") from e

    def get_cursor(self) -> sqlite3.Cursor:
        """
        Get a database cursor
        :return: sqlite3.Cursor
        """
        if not self._cursor:
            raise DatabaseConnectionError("Database session is not open. Call 'open' first.")
        return self._cursor

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection
        :return: sqlite3.Connection
        """
        if not self._connection:
            raise DatabaseConnectionError("Database session is not open. Call 'open' first.")
        return self._connection

    def __enter__(self) -> "SQLiteDatabaseSession":
        """
        Database session enter, opens a new database session

        This method is used in the context manager

        :return: DatabaseSession
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Database session exit, close the database session.
        This method is used in the context manager, and It automatically rolls back
        if exception is raised.


        ref: https://docs.python.org/3.9/reference/datamodel.html?highlight=__exit__#object.__exit__

        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return: None
        """
        if exc_type or exc_val or exc_tb:
            self.rollback()
        self.close()
