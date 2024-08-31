# core/application/services/user_service.py
from __future__ import annotations

from statikk.core.domain.entities.user import User
from statikk.core.domain.repositories.user_repository import UserRepository
from statikk.core.domain.value_objects.user_id import UserID


class UserService:
    """
    Service for handling user-related business logic.

    This service provides operations for retrieving and managing users,
    coordinating with the domain layer entities and repositories.

    :param user_repository: The repository used to interact with user data.
    :type user_repository: UserRepository
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> User:
        """
        Retrieve a user by their unique identifier.

        :param user_id: The unique ID of the user.
        :type user_id: str
        :return: The user associated with the given ID.
        :rtype: User
        :raises ValueError: If the user with the given ID does not exist.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")
        return user

    def create_user(self, username: str, email: str) -> User:
        """
        Create a new user with the specified username and email.

        :param username: The username for the new user.
        :type username: str
        :param email: The email address for the new user.
        :type email: str
        :return: The created user.
        :rtype: User
        """
        user = User(user_id=UserID(), username=username, email=email)
        self.user_repository.save(user)
        return user

    def update_user_email(self, user_id: str, new_email: str) -> User:
        """
        Update the email address of an existing user.

        :param user_id: The unique ID of the user to update.
        :type user_id: str
        :param new_email: The new email address to set for the user.
        :type new_email: str
        :return: The updated user.
        :rtype: User
        :raises ValueError: If the user with the given ID does not exist.
        """
        user = self.get_user(user_id)
        user.email = new_email
        self.user_repository.save(user)
        return user

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user by their unique identifier.

        :param user_id: The unique ID of the user to delete.
        :type user_id: str
        :raises ValueError: If the user with the given ID does not exist.
        """
        user = self.get_user(user_id)
        self.user_repository.delete(user)
