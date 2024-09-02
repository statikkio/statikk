import uuid

class CollectionID:
    """
    Represents a unique identifier for a Collection.

    :param id: The unique ID string. If not provided, a new UUID is generated.
    :type id: str, optional
    """

    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())

    def __eq__(self, other):
        return isinstance(other, CollectionID) and self.id == other.id

    def __str__(self):
        return self.id
