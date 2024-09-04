from __future__ import annotations

import uuid


class ProjectID:
    """
    Represents a unique identifier for a Project.

    :param id: The unique ID string. If not provided, a new UUID is generated.
    :type id: str, optional
    """

    def __init__(self, id: str | None = None):
        """
        Initializes a new ProjectID value object.

        :param id: The unique identifier as a string. If not provided, generates a new UUID.
        :type id: str, optional
        """
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self._validate(id)
            self.id = id

    def _validate(self, id: str):
        """
        Validates the format of the provided ID.

        :param id: The ID string to validate.
        :type id: str
        :raises ValueError: If the ID is not a valid UUID.
        """
        try:
            uuid.UUID(id)
        except ValueError as e:
            raise ValueError(f"Invalid ProjectID: {id}. Must be a valid UUID.") from e

    def __eq__(self, other):
        """
        Checks equality between two ProjectID objects.

        :param other: Another ProjectID object.
        :type other: ProjectID
        :return: True if IDs are equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ProjectID):
            return False
        return self.id == other.id

    def __str__(self):
        """
        Returns the string representation of the ProjectID.

        :return: The ID as a string.
        :rtype: str
        """
        return self.id

    def __repr__(self):
        """
        Returns a detailed string representation of the ProjectID.

        :return: A detailed string representation of the ProjectID.
        :rtype: str
        """
        return f"ProjectID(id='{self.id}')"
