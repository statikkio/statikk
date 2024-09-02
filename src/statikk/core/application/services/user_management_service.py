
from statikk.core.domain.entities.user import User
from statikk.core.domain.repositories.user_repository import UserRepository
from statikk.core.domain.value_objects.user_id import UserID

class UserManagementService:
    """
    Service for handling user-related business logic that does not naturally fit into the User entity.

    :param user_repository: Repository for interacting with user data.
    :type user_repository: UserRepository
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str) -> User:
        """
        Register a new user.

        :param username: The username of the user.
        :param email: The email address of the user.
        :return: The created User object.
        """
        # Business logic for registering a user
        user = User(user_id=UserID(), username=username, email=email)
        self.user_repository.save(user)
        return user
