from __future__ import annotations

from statikk.core.domain.entities.collection import Collection
from statikk.core.domain.repositories.collection_repository import CollectionRepository
from statikk.core.domain.value_objects.collection_id import CollectionID


class CollectionService:
    """
    Service for handling collection-related operations.

    :param collection_repository: Repository for interacting with collection data.
    :type collection_repository: CollectionRepository
    """

    def __init__(self, collection_repository: CollectionRepository):
        self.collection_repository = collection_repository

    def create_collection(self, name: str, schema: dict) -> Collection:
        """
        Create a new collection.

        :param name: The name of the collection.
        :type name: str
        :param schema: The schema of the collection.
        :type schema: dict
        :return: The created Collection object.
        :rtype: Collection
        """
        collection = Collection(
            collection_id=CollectionID(),
            name=name,
            schema=schema,
        )
        self.collection_repository.save(collection)
        return collection

    def get_collection(self, collection_id: str) -> Collection:
        """
        Retrieve a collection by its unique identifier.

        :param collection_id: The unique ID of the collection.
        :type collection_id: str
        :return: The collection associated with the given ID.
        :rtype: Collection
        :raises KeyError: If the collection does not exist.
        """
        return self.collection_repository.get_by_id(CollectionID(collection_id))

    def update_collection(self, collection_id: str, name: str, schema: dict) -> Collection:
        """
        Update an existing collection.

        :param collection_id: The unique ID of the collection.
        :param name: The new name of the collection.
        :type name: str
        :param schema: The new schema for the collection.
        :type schema: dict
        :return: The updated Collection object.
        :rtype: Collection
        :raises KeyError: If the collection does not exist.
        """
        collection = self.get_collection(collection_id)
        collection.name = name
        collection.schema = schema
        self.collection_repository.update(collection)
        return collection

    def delete_collection(self, collection_id: str) -> None:
        """
        Delete a collection by its unique identifier.

        :param collection_id: The unique ID of the collection to delete.
        :type collection_id: str
        :raises KeyError: If the collection does not exist.
        """
        self.collection_repository.delete(CollectionID(collection_id))

    def list_all_collections(self) -> list[Collection]:
        """
        List all collections.

        :return: A list of all collections.
        :rtype: List[Collection]
        """
        # Assuming list_all method exists in the repository
        return self.collection_repository.list_all()
