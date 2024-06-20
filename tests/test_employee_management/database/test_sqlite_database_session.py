import os
import sqlite3
import unittest
from unittest.mock import Mock, patch

from employee_management.core.configurations.configuration import configuration
from employee_management.database.sqlite_database_session import SQLiteDatabaseSession
from employee_management.exceptions.sqlite_database import (
    DatabaseConnectionError,
    DatabaseOperationError,
)


class DatabaseSessionTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URL"] = ":memory:"
        self.db_name = configuration.database_url
        self.db_session = SQLiteDatabaseSession()

    def test_open_success(self):
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.return_value.cursor.return_value = Mock()
            self.db_session.open()
            self.assertIsNotNone(self.db_session.get_connection())
            self.assertIsNotNone(self.db_session.get_cursor())
            mock_connect.assert_called_once_with(self.db_name)

    def test_open_failure(self):
        with patch(
            "sqlite3.connect", side_effect=sqlite3.Error("Connection error")
        ), self.assertRaises(DatabaseConnectionError):
            self.db_session.open()

    def test_rollback_success(self):
        with patch("sqlite3.connect") as mock_connect:
            self.db_session.open()
            self.db_session.rollback()
            mock_connect.return_value.rollback.assert_called_once()

    def test_rollback_failure(self):
        with patch("sqlite3.connect") as mock_connect:
            self.db_session.open()
            with self.assertRaises(DatabaseOperationError) as exception:
                mock_connect.return_value.rollback.side_effect = sqlite3.Error()
                self.db_session.rollback()
                mock_connect.return_value.rollback.assert_called_once()
            self.assertEqual(str(exception.exception), "Failed to rollback changes: ")

    def test_get_cursor_success(self):
        self.db_session.open()
        cursor = self.db_session.get_cursor()
        self.assertIsNotNone(cursor)

    def test_get_cursor_failure(self):
        with self.assertRaises(DatabaseConnectionError):
            self.db_session.get_cursor()

    def test_get_connection_success(self):
        self.db_session.open()
        connection = self.db_session.get_connection()
        self.assertIsNotNone(connection)

    def test_get_connection_failure(self):
        with self.assertRaises(DatabaseConnectionError):
            self.db_session.get_connection()

    def test_context_manager_success(self):
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.return_value.cursor.return_value = Mock()
            with SQLiteDatabaseSession() as db_session:
                self.assertIsNotNone(db_session._connection)
                self.assertIsNotNone(db_session._cursor)
            mock_connect.return_value.cursor.return_value.close.assert_called_once()
            mock_connect.return_value.close.assert_called_once()

    def test_context_manager_with_exception(self):
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.return_value.cursor.return_value = Mock()
            with self.assertRaises(ValueError), SQLiteDatabaseSession() as db_session:
                self.assertIsNotNone(db_session._connection)
                self.assertIsNotNone(db_session._cursor)
                raise ValueError("Test exception")
            mock_connect.return_value.rollback.assert_called_once()
            mock_connect.return_value.cursor.return_value.close.assert_called_once()
            mock_connect.return_value.close.assert_called_once()


class TestDatabaseSessionIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URL"] = ":memory:"
        self.db_name = configuration.database_url
        self.db_session = SQLiteDatabaseSession()

    def test_commit_success(self):
        self.db_session.open()
        cursor = self.db_session.get_cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")
        cursor.fetchall()
        self.db_session.commit()
        cursor.close()


if __name__ == "__main__":
    unittest.main()
