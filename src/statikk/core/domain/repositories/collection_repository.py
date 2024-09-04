from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.collection import Collection
from statikk.core.domain.value_objects.collection_id import CollectionID


class CollectionRepository(ABC):
    """
    Interface for the Collection repository that defines methods to interact with Collection data.
    """

    @abstractmethod
    def get_by_id(self, collection_id: CollectionID) -> Collection:
        pass

    @abstractmethod
    def save(self, collection: Collection) -> None:
        pass

    @abstractmethod
    def update(self, collection: Collection) -> None:
        pass

    @abstractmethod
    def delete(self, collection_id: CollectionID) -> None:
        pass
