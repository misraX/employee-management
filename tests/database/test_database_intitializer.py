import sqlite3
import unittest

from employee_management.core.configurations.configuration import configuration
from employee_management.database.database_initializer import DatabaseInitializer


class DatabaseInitializerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.config = configuration
        self.database_initializer = DatabaseInitializer()

    def test_create_employee_table(self):
        self.database_initializer.create_employee_table()
        conn = sqlite3.connect(self.config.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee';")
