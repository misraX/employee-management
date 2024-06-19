import os
import sqlite3
import unittest
from unittest.mock import Mock, patch

from employee_management_system.core.configurations.configuration import configuration
from employee_management_system.database.database_initializer import DatabaseInitializer


class DatabaseInitializerUnitTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URL"] = ":memory:"
        self.config = configuration
        self.database_initializer = DatabaseInitializer()

    @patch("sqlite3.connect")
    def test_create_employee_table(self, mock_connect: Mock) -> None:
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        db_initializer = DatabaseInitializer()
        db_initializer.create_employee_table()
        mock_connect.assert_called_once_with(":memory:")
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            """
            CREATE TABLE IF NOT EXISTS employee (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                email TEXT NOT NULL,
                salary REAL NOT NULL,
                created_at TEXT NOT NULL,
                modified_at TEXT NOT NULL
            )
        """
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()


class DatabaseInitializerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.config = configuration
        self.database_initializer = DatabaseInitializer()

    def test_create_employee_table(self):
        self.database_initializer.create_employee_table()
        conn = sqlite3.connect(self.config.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee';")
