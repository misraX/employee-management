import abc


class SQLSession(abc.ABC):
    @abc.abstractmethod
    def open(self) -> None:
        """
        Open a database session

        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the database session
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """
        Commit changes to the database
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """
        Rollback changes to the database
        :return: None
        """
        raise NotImplementedError
