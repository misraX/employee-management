import abc
from typing import Generic, TypeVar

T = TypeVar("T")


class Validator(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def validate(self) -> T:
        raise NotImplementedError
