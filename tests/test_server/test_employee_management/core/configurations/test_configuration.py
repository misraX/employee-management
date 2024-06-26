import os
import unittest

from server.employee_management.core.configurations.configuration import Configuration


class ConfigurationTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Configuration()

    def test_configuration_database_url(self):
        os.environ["DATABASE_URL"] = ":memory:"
        self.assertEqual(self.config.database_url, ":memory:")

    def test_configuration_database_name_from_path(self):
        os.environ["DATABASE_URL"] = "employee_management.db"
        self.assertEqual(
            self.config.database_url,
            os.path.join(self.config.base_dir, os.environ.get("DATABASE_URL")),
        )

    def test_configuration_app_name(self):
        os.environ["APP_NAME"] = "Test Application"
        self.assertEqual(self.config.app_name, "Test Application")


if __name__ == "__main__":
    unittest.main()
