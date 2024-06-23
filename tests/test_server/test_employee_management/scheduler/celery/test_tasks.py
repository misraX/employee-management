import unittest
import uuid
from unittest.mock import MagicMock, patch

from server.employee_management.scheduler.celery.tasks import employee_upcoming_holidays


class EmployeeUpcomingHolidaysTaskTestCase(unittest.TestCase):
    @patch("server.employee_management.scheduler.celery.tasks.EmployeeService")
    @patch("server.employee_management.scheduler.celery.tasks.PyPiHolidaysBackend")
    @patch("server.employee_management.scheduler.celery.tasks.NotifyByEmail")
    @patch("server.employee_management.scheduler.celery.tasks.EmployeeSQLiteRepository")
    def test_employee_upcoming_holidays_with_egypt_holidays(
        self,
        mock_employee_repository,
        mock_notify_by_email,
        mock_holidays_backend,
        mock_employee_service,
    ):
        # Arrange
        mock_employee_service_instance = mock_employee_service.return_value
        mock_holidays_backend_instance = mock_holidays_backend.return_value
        mock_employee_repository_instance = mock_employee_repository.return_value

        employee_1_id = uuid.uuid4()
        employee_2_id = uuid.uuid4()

        # Mimic the behavior of get_all with pagination
        mock_employee_repository_instance.get_all.side_effect = [
            [
                MagicMock(employee_id=employee_1_id, email="test1@example.com", country="EG"),
                MagicMock(employee_id=employee_2_id, email="test2@example.com", country="EG"),
            ],
            [],
        ]

        mock_holidays_backend_instance.get_upcoming_holidays.return_value = [
            ("2024-07-23", "Revolution Day"),
            ("2024-01-07", "Coptic Christmas"),
        ]

        # Ensure the service uses the mocked repository
        mock_employee_service_instance.get_all_employees.side_effect = (
            lambda offset, limit: mock_employee_repository_instance.get_all(offset, limit)
        )
        notify_by_email_calls = []

        def mock_notify_by_email_init(*args, **kwargs):
            instance = MagicMock()
            instance.message = kwargs["message"]
            instance.to_email = kwargs["to_email"]
            instance.send = MagicMock()
            notify_by_email_calls.append(instance)
            return instance

        mock_notify_by_email.side_effect = mock_notify_by_email_init
        employee_upcoming_holidays()

        self.assertEqual(mock_employee_repository_instance.get_all.call_count, 2)
        self.assertEqual(mock_holidays_backend_instance.get_upcoming_holidays.call_count, 2)
        self.assertEqual(len(notify_by_email_calls), 2)

        emails_sent_to = [call.to_email for call in notify_by_email_calls]
        self.assertIn("test1@example.com", emails_sent_to)
        self.assertIn("test2@example.com", emails_sent_to)

        self.assertEqual(mock_notify_by_email.call_count, 2)

        for call in notify_by_email_calls:
            self.assertIn("Your upcoming public holidays are as follows:", call.message)
            self.assertIn("Date: 2024-07-23 - Holiday: Revolution Day", call.message)
            self.assertIn("Date: 2024-01-07 - Holiday: Coptic Christmas", call.message)
            call.send.assert_called_once()

        send_call_count = sum([call.send.call_count for call in notify_by_email_calls])
        self.assertEqual(send_call_count, 2)


if __name__ == "__main__":
    unittest.main()
