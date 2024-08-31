from __future__ import annotations

from statikk.core.domain.value_objects import UserID


class User:
    """
    Represents a User in the system.

    :param user_id: Unique identifier for the user.
    :type user_id: UserID
    :param username: The username of the user.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    """

    def __init__(self, user_id: UserID, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
