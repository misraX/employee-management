import abc


class Notify(abc.ABC):
    """
    Abstract base class for sending notifications.
    """

    @abc.abstractmethod
    def send(self):
        """
        Send the notification.
        :return: None
        """
        raise NotImplementedError
