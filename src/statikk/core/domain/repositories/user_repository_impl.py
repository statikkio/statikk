# infrastructure/database/user_repository_impl.py
from __future__ import annotations

from statikk.core.domain.entities.user import User
from statikk.core.domain.repositories.user_repository import UserRepository


class SubrrealDBUserRepository(UserRepository):
    """
    Implementation of UserRepository that uses SubrrrealDB for data storage.

    :param db_client: The database client used to interact with SubrrrealDB.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client):
        self.db_client = db_client

    def get_by_id(self, user_id: str) -> User:
        """
        Retrieve a user by their unique identifier from SubrrrealDB.

        :param user_id: The unique ID of the user.
        :type user_id: str
        :return: The user associated with the given ID.
        :rtype: User
        """
        # Implement retrieval from SubrrrealDB
        raise NotImplementedError

    def save(self, user: User) -> None:
        """
        Save a user entity to SubrrrealDB.

        :param user: The user entity to save.
        :type user: User
        """
        # Implement save logic to SubrrrealDB
        raise NotImplementedError
