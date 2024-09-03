import uuid


class CloudFunctionID:
    """
    Represents a unique identifier for a CloudFunction.

    :param id: The unique ID string. If not provided, a new UUID is generated.
    :type id: str, optional
    """

    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())

    def __eq__(self, other):
        return isinstance(other, CloudFunctionID) and self.id == other.id

    def __str__(self):
        return self.id
