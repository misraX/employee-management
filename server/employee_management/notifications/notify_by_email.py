import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from server.employee_management.core.configurations.configuration import configuration
from server.employee_management.logging.logger import format_logger_name
from server.employee_management.notifications.notify import Notify

logger = logging.getLogger(format_logger_name("email_notification"))

config = configuration


class NotifyByEmail(Notify):
    """
    Concrete class for sending email notifications.
    """

    def __init__(
        self,
        message,
        to_email,
        from_email,
        subject,
        smtp_server,
        smtp_port,
        smtp_user,
        smtp_password,
    ):
        """
        Initializes the NotifyByEmail class with email-specific attributes.

        :param message (str): The message content of the notification.
        :param to_email (str): The recipient's email address.
        :param from_email (str): The sender's email address.
        :param subject (str): The subject of the email.
        :param smtp_server (str): The SMTP server address.
        :param smtp_port (int): The SMTP server port.
        :param smtp_user (str): The SMTP server username.
        :param smtp_password (str): The SMTP server password.
        """
        self.message = message
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send(self):
        """
        Sends the email notification using the configured SMTP server.

        :raises Exception: if the email failed to send.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = self.to_email
            msg["Subject"] = self.subject
            msg.attach(MIMEText(self.message, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, self.to_email, msg.as_string())
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.warning(f"Failed to send email: {e}")
