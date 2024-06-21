import unittest
from unittest.mock import patch

from faker import Faker

from server.employee_management.notifications.notify_by_email import NotifyByEmail

faker = Faker()


class NotifyByEmailTestCase(unittest.TestCase):
    def setUp(self):
        self.message = "This is a test notification."
        self.to_email = faker.email()
        self.from_email = faker.email()
        self.subject = faker.word()
        self.smtp_server = faker.url()
        self.smtp_port = 587
        self.smtp_user = faker.user_name()
        self.smtp_password = faker.password()

        self.notifier = NotifyByEmail(
            self.message,
            self.to_email,
            self.from_email,
            self.subject,
            self.smtp_server,
            self.smtp_port,
            self.smtp_user,
            self.smtp_password,
        )

    @patch("smtplib.SMTP")
    def test_send_email_successful(self, mock_smtp):
        # context so it must use __enter__
        mock_server = mock_smtp.return_value.__enter__.return_value

        self.notifier.send()

        mock_smtp.assert_called_with(self.smtp_server, self.smtp_port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.smtp_user, self.smtp_password)
        mock_server.sendmail.assert_called_once()
        called_args = mock_server.sendmail.call_args[0]
        self.assertEqual(called_args[0], self.from_email)
        self.assertEqual(called_args[1], self.to_email)
        msg = called_args[2]
        self.assertIn(self.message, msg)

    @patch("smtplib.SMTP")
    def test_send_email_failure(self, mock_smtp):
        # context so it must use __enter__
        mock_server = mock_smtp.return_value.__enter__.return_value
        # Make it fail
        mock_server.sendmail.side_effect = Exception("SMTP error")

        with self.assertLogs("root", level="WARNING") as cm:
            self.notifier.send()

        mock_smtp.assert_called_with(self.smtp_server, self.smtp_port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.smtp_user, self.smtp_password)
        mock_server.sendmail.assert_called_once()
        self.assertIn("WARNING:root:Failed to send email: SMTP error", cm.output)


if __name__ == "__main__":
    unittest.main()
