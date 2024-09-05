# infrastructure/database/collection_repository_impl.py
from __future__ import annotations

from statikk.core.domain.entities.collection import Collection
from statikk.core.domain.repositories.collection_repository import CollectionRepository
from statikk.core.domain.value_objects.collection_id import CollectionID
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient


class SubrrealDBCollectionRepository(CollectionRepository):
    """
    Implementation of CollectionRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, collection_id: CollectionID) -> Collection:
        """
        Retrieve a collection by its unique identifier.

        :param collection_id: The unique ID of the collection.
        :type collection_id: CollectionID
        :return: The collection associated with the given ID.
        :rtype: Collection
        :raises KeyError: If the collection does not exist.
        """
        try:
            query = f"SELECT * FROM collections WHERE id = '{collection_id}'"
            result = self.db_client.query(query)
            if not result:
                raise KeyError(f"Collection with ID {collection_id} not found.")
            return Collection(
                collection_id=CollectionID(result['id']),
                name=result['name'],
                schema=result['schema'],
            )
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to retrieve collection: {str(e)}")
            raise Exception(f"Database error: Could not retrieve collection with ID {collection_id}.") from e

    def save(self, collection: Collection) -> None:
        """
        Save a collection entity to the database.

        :param collection: The collection entity to save.
        :type collection: Collection
        """
        try:
            self.db_client.insert(
                collection='collections',
                data={
                    'id': str(collection.collection_id),
                    'name': collection.name,
                    'schema': collection.schema,
                },
            )
            print(f"Collection {collection.name} saved successfully.")
        except Exception as e:
            print(f"Failed to save collection: {str(e)}")
            raise Exception(f"Database error: Could not save collection {collection.name}.") from e

    def update(self, collection: Collection) -> None:
        """
        Update an existing collection entity in the database.

        :param collection: The collection entity to update.
        :type collection: Collection
        """
        try:
            existing_collection = self.get_by_id(collection.collection_id)
            if not existing_collection:
                raise KeyError(f"Collection with ID {collection.collection_id} not found for update.")

            self.db_client.update(
                collection='collections',
                identifier=str(collection.collection_id),
                data={
                    'name': collection.name,
                    'schema': collection.schema,
                },
            )
            print(f"Collection {collection.name} updated successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to update collection: {str(e)}")
            raise Exception(f"Database error: Could not update collection with ID {collection.collection_id}.") from e

    def delete(self, collection_id: CollectionID) -> None:
        """
        Delete a collection by its unique identifier.

        :param collection_id: The unique ID of the collection to delete.
        :type collection_id: CollectionID
        """
        try:
            existing_collection = self.get_by_id(collection_id)
            if not existing_collection:
                raise KeyError(f"Collection with ID {collection_id} not found for deletion.")

            self.db_client.delete(
                collection='collections',
                identifier=str(collection_id),
            )
            print(f"Collection with ID {collection_id} deleted successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to delete collection: {str(e)}")
            raise Exception(f"Database error: Could not delete collection with ID {collection_id}.") from e
