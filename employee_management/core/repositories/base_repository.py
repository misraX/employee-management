import abc
import uuid
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(abc.ABC):  # noqa
    """
    Abstract base class for repositories.
    """


class CRUDRepository(Repository, Generic[T]):
    """
    Abstract base class for CRUD operation repositories.
    """

    @abc.abstractmethod
    def get(self, entity_id: uuid.UUID) -> T:
        """
        Get entity by ID.

        :param entity_id: uuid.UUID
        :return: T
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity_id: uuid.UUID) -> None:
        """
        Delete entity by ID.

        :param entity_id: uuid.UUID
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, entity: T) -> T:
        """
        Add entity to repository.

        :param entity: T
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, entity_id: uuid.UUID, update: dict) -> T:
        """
        Update entity in repository.

        :param entity_id: uuid.UUID
        :param update: dict of updates (table_column: value)
        """
        raise NotImplementedError
