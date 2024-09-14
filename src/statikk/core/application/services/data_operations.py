from __future__ import annotations

from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient
from statikk.infrastructure.realtime.realtime_server import manager


class DataOperations:
    """
    Handles CRUD operations on the database and emits real-time updates.

    Attributes:
        db_manager (SubrrealDBManager): The manager for handling project-specific database connections.
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    async def create_document(self, collection: str, document: dict):
        """
        Creates a new document in a specified collection and sends a real-time update.

        :param project_id: The unique identifier of the project.
        :type project_id: str
        :param collection: The collection where the document will be inserted.
        :type collection: str
        :param document: The document data to insert.
        :type document: dict
        """
        self.db_client.insert(collection, document)
        await manager.send_update(collection, {'action': 'create', 'document': document})

    async def update_document(self, collection: str, document_id: str, update: dict):
        """
        Updates a document in a specified collection and sends a real-time update.

        :param project_id: The unique identifier of the project.
        :type project_id: str
        :param collection: The collection where the document is located.
        :type collection: str
        :param document_id: The unique identifier of the document to update.
        :type document_id: str
        :param update: The update data to apply to the document.
        :type update: dict
        """
        self.db_client.update(collection, {'_id': document_id}, update)
        await manager.send_update(collection, {'action': 'update', 'document_id': document_id, 'update': update})

    async def delete_document(self, collection: str, document_id: str):
        """
        Deletes a document from a specified collection and sends a real-time update.

        :param project_id: The unique identifier of the project.
        :type project_id: str
        :param collection: The collection from which the document will be deleted.
        :type collection: str
        :param document_id: The unique identifier of the document to delete.
        :type document_id: str
        """
        self.db_client.delete(collection, {'_id': document_id})
        await manager.send_update(collection, {'action': 'delete', 'document_id': document_id})
