from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.user import User


class UserRepository(ABC):
    """
    Interface for user repository that defines methods to interact with user data.

    Methods should be implemented by concrete classes that connect to a database.
    """

    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        """
        Retrieve a user by their unique identifier.
        """
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        """
        Save a user entity to the repository.
        """
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """
        Delete a user entity from the repository.

        :param user: The user entity to delete.
        :type user: User
        """
        pass
