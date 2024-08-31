# interfaces/api/controllers/user_controller.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from statikk.core.application.services.user_service import UserService
from statikk.core.domain.repositories.user_repository import UserRepository


# Dependency Injection of UserService
# Dependency Injection function for UserService
def get_user_service(repository: Annotated[UserRepository, Depends()]) -> UserService:
    """
    Provides an instance of UserService for dependency injection.

    :return: An instance of UserService.
    :rtype: UserService
    """
    return UserService(repository)


# Pydantic models for request and response bodies


class UserCreateRequest(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str


# Initialize the APIRouter for user-related endpoints
user_router = APIRouter()


@user_router.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    """
    Endpoint to retrieve a user by their unique identifier.

    :param user_id: The unique ID of the user.
    :type user_id: str
    :param user_service: The service used to handle user-related operations.
    :type user_service: UserService
    :return: A UserResponse object containing the user's details.
    :rtype: UserResponse
    :raises HTTPException: If the user does not exist.
    """
    try:
        user = user_service.get_user(user_id)
        return UserResponse(user_id=user.user_id.id, username=user.username, email=user.email)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e),
        )


@user_router.post('/users', response_model=UserResponse)
async def create_user(request: UserCreateRequest, user_service: UserService = Depends(get_user_service)):
    """
    Endpoint to create a new user.

    :param request: The request body containing username and email.
    :type request: UserCreateRequest
    :param user_service: The service used to handle user-related operations.
    :type user_service: UserService
    :return: A UserResponse object with the created user's details.
    :rtype: UserResponse
    """
    user = user_service.create_user(
        username=request.username, email=request.email,
    )
    return UserResponse(user_id=user.user_id.id, username=user.username, email=user.email)


@user_router.put('/users/{user_id}/email', response_model=UserResponse)
async def update_user_email(user_id: str, new_email: str, user_service: UserService = Depends(get_user_service)):
    """
    Endpoint to update a user's email address.

    :param user_id: The unique ID of the user to update.
    :type user_id: str
    :param new_email: The new email address to set for the user.
    :type new_email: str
    :param user_service: The service used to handle user-related operations.
    :type user_service: UserService
    :return: A UserResponse object with the updated user's details.
    :rtype: UserResponse
    :raises HTTPException: If the user does not exist.
    """
    try:
        user = user_service.update_user_email(user_id, new_email)
        return UserResponse(user_id=user.user_id.id, username=user.username, email=user.email)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e),
        )


@user_router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    """
    Endpoint to delete a user by their unique identifier.

    :param user_id: The unique ID of the user to delete.
    :type user_id: str
    :param user_service: The service used to handle user-related operations.
    :type user_service: UserService
    :raises HTTPException: If the user does not exist.
    """
    try:
        user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e),
        )
