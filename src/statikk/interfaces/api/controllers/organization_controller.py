from fastapi import APIRouter, Depends, HTTPException, status
from statikk.core.application.services.organization_service import OrganizationService
from pydantic import BaseModel
from typing import List, Dict

# Initialize the APIRouter for organizations
router = APIRouter()

# Pydantic models for request and response bodies
class OrganizationRequest(BaseModel):
    name: str
    owner_id: str

class OrganizationResponse(BaseModel):
    organization_id: str
    name: str
    owner_id: str
    members: Dict[str, str]

class AddMemberRequest(BaseModel):
    user_id: str
    role: str

@router.post("/organizations", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(request: OrganizationRequest, service: OrganizationService = Depends()):
    """
    Create a new organization.

    :param request: The request body containing the organization's name and owner ID.
    :type request: OrganizationRequest
    :param service: The service used to handle organization-related operations.
    :type service: OrganizationService
    :return: The created organization details.
    :rtype: OrganizationResponse
    """
    try:
        organization = service.create_organization(name=request.name, owner_id=request.owner_id)
        return OrganizationResponse(
            organization_id=str(organization.organization_id),
            name=organization.name,
            owner_id=str(organization.owner_id),
            members={str(k): v for k, v in organization.members.items()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/organizations/{organization_id}", response_model=OrganizationResponse)
async def get_organization(organization_id: str, service: OrganizationService = Depends()):
    """
    Retrieve an organization by its unique identifier.

    :param organization_id: The unique ID of the organization.
    :type organization_id: str
    :param service: The service used to handle organization-related operations.
    :type service: OrganizationService
    :return: The organization details.
    :rtype: OrganizationResponse
    :raises HTTPException: If the organization does not exist.
    """
    try:
        organization = service.get_organization(organization_id)
        return OrganizationResponse(
            organization_id=str(organization.organization_id),
            name=organization.name,
            owner_id=str(organization.owner_id),
            members={str(k): v for k, v in organization.members.items()}
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/organizations/{organization_id}", response_model=OrganizationResponse)
async def update_organization(organization_id: str, request: OrganizationRequest, service: OrganizationService = Depends()):
    """
    Update an existing organization.

    :param organization_id: The unique ID of the organization.
    :type organization_id: str
    :param request: The request body containing the new organization's name.
    :type request: OrganizationRequest
    :param service: The service used to handle organization-related operations.
    :type service: OrganizationService
    :return: The updated organization details.
    :rtype: OrganizationResponse
    :raises HTTPException: If the organization does not exist.
    """
    try:
        updated_organization = service.update_organization(organization_id, name=request.name)
        return OrganizationResponse(
            organization_id=str(updated_organization.organization_id),
            name=updated_organization.name,
            owner_id=str(updated_organization.owner_id),
            members={str(k): v for k, v in updated_organization.members.items()}
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/organizations/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(organization_id: str, service: OrganizationService = Depends()):
    """
    Delete an organization by its unique identifier.

    :param organization_id: The unique ID of the organization to delete.
    :type organization_id: str
    :param service: The service used to handle organization-related operations.
    :type service: OrganizationService
    :raises HTTPException: If the organization does not exist.
    """
    try:
        service.delete_organization(organization_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/organizations/{organization_id}/members", response_model=OrganizationResponse)
async def add_member(organization_id: str, request: AddMemberRequest, service: OrganizationService = Depends()):
    """
    Add a member to the organization.

    :param organization_id: The unique ID of the organization.
    :type organization_id: str
    :param request: The request body containing the user's ID and role.
    :type request: AddMemberRequest
    :param service: The service used to handle organization-related operations.
    :type service: OrganizationService
    :return: The updated organization details.
    :rtype: OrganizationResponse
    """
    try:
        organization = service.add_member(organization_id, user_id=request.user_id, role=request.role)
        return OrganizationResponse(
            organization_id=str(organization.organization_id),
            name=organization.name,
            owner_id=str(organization.owner_id),
            members={str(k): v for k, v in organization.members.items()}
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
