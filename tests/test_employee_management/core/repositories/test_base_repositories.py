import unittest
import uuid
from typing import Final
from unittest import TestCase
from uuid import UUID

from employee_management.core.repositories.base_repository import CRUDRepository, T
from employee_management.exceptions.immutable import ImmutableAttributeError


class Entity:
    def __init__(self, name: str, entity_id: uuid.UUID | None = None):
        self._name: Final[str] = name
        self._id: Final[uuid.UUID] = entity_id if entity_id else uuid.uuid4()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        raise ImmutableAttributeError("Cannot modify the name attribute.")

    @property
    def id(self) -> uuid.UUID:
        return self._id


class EntityRepository(CRUDRepository[Entity]):
    def __init__(self):
        self._entities: dict[uuid.UUID, dict] = {}

    def get(self, entity_id: uuid.UUID) -> T | None:
        return self._entities.get(entity_id)

    def delete(self, entity_id: uuid.UUID) -> None:
        return self._entities.pop(entity_id, None)

    def add(self, entity: T) -> T:
        self._entities[entity.id] = dict(name=entity.name, id=entity.id)
        return entity

    def update(self, entity_id: uuid.UUID, update: dict) -> T:
        if entity_id not in self._entities:
            raise KeyError
        self._entities[entity_id].update(update)
        return update

    def get_all(self) -> dict[UUID, dict]:
        return self._entities


class TestCRUDRepository(TestCase):
    def setUp(self):
        self.repository = EntityRepository()
        self.entity = Entity("test")
        self.entity2 = Entity("test2")

    def test_add(self):
        self.repository.add(self.entity)
        self.assertEqual(
            dict(name=self.entity.name, id=self.entity.id), self.repository.get(self.entity.id)
        )
        self.assertEqual(self.entity.name, self.repository.get(self.entity.id).get("name"))

    def test_update(self):
        self.repository.add(self.entity)
        updates = dict(name="Modified test")
        self.repository.update(entity_id=self.entity.id, update=updates)
        entity = self.repository.get(self.entity.id)
        self.assertEqual(entity.get("name"), updates.get("name"))

    def test_delete(self):
        self.repository.add(self.entity)
        self.repository.delete(self.entity.id)
        entity = self.repository.get(self.entity.id)
        self.assertIsNone(entity)

    def test_get_all(self):
        self.repository.add(self.entity)
        self.repository.add(self.entity2)
        entities = self.repository.get_all()
        self.assertEqual(len(entities), 2)

    def test_immutable_entity_attr(self):
        self.repository.add(self.entity)
        with self.assertRaises(AttributeError) as attribute_error:
            self.entity.name = "Modified test"
        self.assertEqual(attribute_error.exception.__str__(), "Cannot modify the name attribute.")


if __name__ == "__main__":
    unittest.main()
