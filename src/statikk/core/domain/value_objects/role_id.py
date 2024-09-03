import uuid

class RoleID:
    """
    Represents a unique identifier for a Role.

    :param id: The unique ID string. If not provided, a new UUID is generated.
    :type id: str, optional
    """

    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())

    def __eq__(self, other):
        return isinstance(other, RoleID) and self.id == other.id

    def __str__(self):
        return self.id
