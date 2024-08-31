# tests/unit/test_user_service.py
from __future__ import annotations

from unittest.mock import Mock

import pytest
from statikk.core.application.services.user_service import UserService
from statikk.core.domain.entities.user import User
from statikk.core.domain.repositories.user_repository import UserRepository
from statikk.core.domain.value_objects.user_id import UserID


@pytest.fixture
def mock_user_repository():
    """
    Fixture to create a mock user repository.

    :return: A mock user repository instance.
    :rtype: Mock
    """
    return Mock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    """
    Fixture to create a UserService instance with a mock repository.

    :param mock_user_repository: The mock repository instance.
    :type mock_user_repository: Mock
    :return: A UserService instance.
    :rtype: UserService
    """
    return UserService(user_repository=mock_user_repository)


def test_get_user_success(user_service, mock_user_repository):
    """
    Test retrieving a user successfully.

    :param user_service: The UserService instance.
    :param mock_user_repository: The mock user repository.
    """
    # Arrange
    user_id = UserID('1234')
    expected_user = User(
        user_id=user_id, username='testuser', email='test@example.com',
    )
    mock_user_repository.get_by_id.return_value = expected_user

    # Act
    user = user_service.get_user(user_id.id)

    # Assert
    assert user == expected_user
    mock_user_repository.get_by_id.assert_called_once_with(user_id.id)


def test_get_user_not_found(user_service, mock_user_repository):
    """
    Test retrieving a user that does not exist.

    :param user_service: The UserService instance.
    :param mock_user_repository: The mock user repository.
    """
    # Arrange
    user_id = UserID('1234')
    mock_user_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match=f"User with ID {user_id.id} does not exist."):
        user_service.get_user(user_id.id)


def test_create_user(user_service, mock_user_repository):
    """
    Test creating a new user.

    :param user_service: The UserService instance.
    :param mock_user_repository: The mock user repository.
    """
    # Arrange
    username = 'newuser'
    email = 'newuser@example.com'

    # Act
    user = user_service.create_user(username=username, email=email)

    # Assert
    assert user.username == username
    assert user.email == email
    assert isinstance(user.user_id, UserID)
    mock_user_repository.save.assert_called_once_with(user)


def test_update_user_email(user_service, mock_user_repository):
    """
    Test updating an existing user's email.

    :param user_service: The UserService instance.
    :param mock_user_repository: The mock user repository.
    """
    # Arrange
    user_id = UserID('1234')
    existing_user = User(
        user_id=user_id, username='testuser', email='old@example.com',
    )
    mock_user_repository.get_by_id.return_value = existing_user
    new_email = 'new@example.com'

    # Act
    updated_user = user_service.update_user_email(user_id.id, new_email)

    # Assert
    assert updated_user.email == new_email
    mock_user_repository.get_by_id.assert_called_once_with(user_id.id)
    mock_user_repository.save.assert_called_once_with(updated_user)


def test_delete_user(user_service, mock_user_repository):
    """
    Test deleting a user.

    :param user_service: The UserService instance.
    :param mock_user_repository: The mock user repository.
    """
    # Arrange
    user_id = UserID('1234')
    existing_user = User(
        user_id=user_id, username='testuser', email='test@example.com',
    )
    mock_user_repository.get_by_id.return_value = existing_user

    # Act
    user_service.delete_user(user_id.id)

    # Assert
    mock_user_repository.get_by_id.assert_called_once_with(user_id.id)
    mock_user_repository.delete.assert_called_once_with(existing_user)
