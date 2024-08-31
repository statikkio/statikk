from __future__ import annotations

from uuid import uuid4


class UserID:
    """
    Represents a unique identifier for a User.

    :param id: The unique ID string. If not provided, a new UUID is generated.
    :type id: Optional[str]
    """

    def __init__(self, id: str | None = None):
        self.id = id or str(uuid4())

    def __str__(self):
        return self.id
