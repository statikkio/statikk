# interfaces/api/controllers/role_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from statikk.core.application.services.organization_service import OrganizationService
from statikk.core.domain.entities.role import Role
from statikk.core.domain.value_objects.permissions import Permission
from statikk.core.domain.value_objects.role_id import RoleID
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic models for request and response bodies


class RoleRequest(BaseModel):
    name: str
    permissions: List[str]


class RoleResponse(BaseModel):
    role_id: str
    name: str
    permissions: List[str]


class AssignRoleRequest(BaseModel):
    user_id: str
    role_id: str


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(request: RoleRequest, service: OrganizationService = Depends()):
    """
    Create a new role with specified permissions.

    :param request: The request body containing the role's name and permissions.
    :type request: RoleRequest
    :param service: The service used to handle role-related operations.
    :type service: OrganizationService
    :return: The created role details.
    :rtype: RoleResponse
    """
    try:
        role = Role(
            role_id=RoleID(),
            name=request.name,
            permissions=[Permission(name) for name in request.permissions]
        )
        # Assuming you have a method in the service to handle role saving
        service.organization_repository.save_role(role)  # This should be handled within the appropriate service/repository
        return RoleResponse(
            role_id=str(role.role_id),
            name=role.name,
            permissions=[str(p) for p in role.permissions]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: str, service: OrganizationService = Depends()):
    """
    Retrieve a role by its unique identifier.

    :param role_id: The unique ID of the role.
    :type role_id: str
    :param service: The service used to handle role-related operations.
    :type service: OrganizationService
    :return: The role details.
    :rtype: RoleResponse
    :raises HTTPException: If the role does not exist.
    """
    try:
        role = service.organization_repository.get_role_by_id(RoleID(role_id))  # Retrieve role using the repository
        return RoleResponse(
            role_id=str(role.role_id),
            name=role.name,
            permissions=[str(p) for p in role.permissions]
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: str, request: RoleRequest, service: OrganizationService = Depends()):
    """
    Update an existing role's name and permissions.

    :param role_id: The unique ID of the role.
    :type role_id: str
    :param request: The request body containing the new role's name and permissions.
    :type request: RoleRequest
    :param service: The service used to handle role-related operations.
    :type service: OrganizationService
    :return: The updated role details.
    :rtype: RoleResponse
    :raises HTTPException: If the role does not exist.
    """
    try:
        role = service.organization_repository.get_role_by_id(RoleID(role_id))
        role.name = request.name
        role.permissions = [Permission(name) for name in request.permissions]
        service.organization_repository.update_role(role)  # Update the role using the repository
        return RoleResponse(
            role_id=str(role.role_id),
            name=role.name,
            permissions=[str(p) for p in role.permissions]
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: str, service: OrganizationService = Depends()):
    """
    Delete a role by its unique identifier.

    :param role_id: The unique ID of the role to delete.
    :type role_id: str
    :param service: The service used to handle role-related operations.
    :type service: OrganizationService
    :raises HTTPException: If the role does not exist.
    """
    try:
        service.organization_repository.delete_role(RoleID(role_id))  # Delete the role using the repository
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/organizations/{organization_id}/members/{user_id}/roles", response_model=RoleResponse)
async def assign_role_to_member(
    organization_id: str,
    user_id: str,
    request: AssignRoleRequest,
    service: OrganizationService = Depends()
):
    """
    Assign a role to a member of the organization.

    :param organization_id: The unique ID of the organization.
    :type organization_id: str
    :param user_id: The unique ID of the user.
    :type user_id: str
    :param request: The request body containing the role's ID to assign.
    :type request: AssignRoleRequest
    :param service: The service used to handle role-related operations.
    :type service: OrganizationService
    :return: The updated role details.
    :rtype: RoleResponse
    :raises HTTPException: If the role or organization does not exist.
    """
    try:
        role = service.organization_repository.get_role_by_id(RoleID(request.role_id))
        organization = service.assign_role_to_member(organization_id, user_id, role)
        return RoleResponse(
            role_id=str(role.role_id),
            name=role.name,
            permissions=[str(p) for p in role.permissions]
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or organization not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
