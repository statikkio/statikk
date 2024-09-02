# infrastructure/database/user_repository_impl.py
from statikk.core.domain.entities.user import User
from statikk.core.domain.repositories.user_repository import UserRepository
from statikk.core.domain.value_objects.user_id import UserID
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient

class SubrrealDBUserRepository(UserRepository):
    """
    Implementation of UserRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, user_id: UserID) -> User:
        """
        Retrieve a user by their unique identifier.

        :param user_id: The unique ID of the user.
        :type user_id: UserID
        :return: The user associated with the given ID.
        :rtype: User
        :raises KeyError: If the user does not exist.
        """
        try:
            query = f"SELECT * FROM users WHERE id = '{user_id}'"
            result = self.db_client.query(query)
            if not result:
                raise KeyError(f"User with ID {user_id} not found.")
            return User(
                user_id=UserID(result['id']),
                username=result['username'],
                email=result['email']
            )
        except Exception as e:
            raise KeyError(f"Failed to retrieve user: {str(e)}")

    def save(self, user: User) -> None:
        """
        Save a user entity to the database.

        :param user: The user entity to save.
        :type user: User
        """
        try:
            self.db_client.insert(
                collection="users",
                data={
                    "id": str(user.user_id),
                    "username": user.username,
                    "email": user.email
                }
            )
            print(f"User {user.username} saved successfully.")
        except Exception as e:
            raise Exception(f"Failed to save user: {str(e)}")

    def update(self, user: User) -> None:
        """
        Update an existing user entity in the database.

        :param user: The user entity to update.
        :type user: User
        """
        try:
            self.db_client.update(
                collection="users",
                identifier=str(user.user_id),
                data={
                    "username": user.username,
                    "email": user.email
                }
            )
            print(f"User {user.username} updated successfully.")
        except Exception as e:
            raise Exception(f"Failed to update user: {str(e)}")

    def delete(self, user_id: UserID) -> None:
        """
        Delete a user by their unique identifier.

        :param user_id: The unique ID of the user to delete.
        :type user_id: UserID
        """
        try:
            self.db_client.delete(
                collection="users",
                identifier=str(user_id)
            )
            print(f"User with ID {user_id} deleted successfully.")
        except Exception as e:
            raise Exception(f"Failed to delete user: {str(e)}")
