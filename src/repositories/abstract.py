from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    def create(self, data: dict, *args, **kwargs):
        """create entity in the database"""

    @abstractmethod
    def update(self, entity_id: int, data: dict, *args, **kwargs):
        """update entity"""

    @abstractmethod
    def delete(self, entity_id: int, *args, **kwargs):
        """delete entity from the database"""

    @abstractmethod
    def find_all(self, *args, **kwargs):
        """get list of entities"""

    @abstractmethod
    def find_by_id(self, entity_id: int, *args, **kwargs):
        """retrieve some instance if exists"""
