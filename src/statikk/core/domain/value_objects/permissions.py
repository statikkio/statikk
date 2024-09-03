
class Permission:
    """
    Represents a specific permission that can be assigned to a role.

    :param name: The name of the permission (e.g., "create_collection").
    :type name: str
    """

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Permission) and self.name == other.name

    def __str__(self):
        return self.name
