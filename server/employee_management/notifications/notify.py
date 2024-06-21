import abc


class Notify(abc.ABC):
    """
    Abstract base class for sending notifications.
    """

    def __init__(self, message: str):
        """
        Abstract base class for sending notifications.

        :param message: Message to be sent.
        """
        self.message = message

    @abc.abstractmethod
    def send(self):
        """
        Send the notification.
        :return: None
        """
        raise NotImplementedError
