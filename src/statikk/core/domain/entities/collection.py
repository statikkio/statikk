from __future__ import annotations

from statikk.core.domain.value_objects import CollectionID


class Collection:
    """
    Represents a data collection in the system, similar to a database table.

    :param collection_id: Unique identifier for the collection.
    :type collection_id: CollectionID
    :param name: The name of the collection.
    :type name: str
    :param schema: The schema of the collection, defining the structure of the data.
    :type schema: dict
    """

    def __init__(self, collection_id: CollectionID, name: str, schema: dict):
        self.collection_id = collection_id
        self.name = name
        self.schema = schema

    def add_field(self, field_name: str, field_type: str):
        """
        Add a field to the collection schema.

        :param field_name: The name of the field to add.
        :type field_name: str
        :param field_type: The type of the field (e.g., string, integer).
        :type field_type: str
        """
        self.schema[field_name] = field_type
