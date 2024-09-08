from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from statikk.core.application.services.project_config_service import ProjectConfigService

router = APIRouter()

# Pydantic models for request and response bodies


class ProjectConfigRequest(BaseModel):
    config: dict[str, str]


class ProjectConfigResponse(BaseModel):
    project_id: str
    config: dict[str, str]


@router.post('/projects/{project_id}/config', response_model=ProjectConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_project_config(project_id: str, request: ProjectConfigRequest, service: ProjectConfigService = Depends()):
    """
    Create a new project configuration.

    :param project_id: The unique ID of the project.
    :type project_id: str
    :param request: The request body containing the configuration keys and values.
    :type request: ProjectConfigRequest
    :param service: The service used to handle project configuration-related operations.
    :type service: ProjectConfigService
    :return: The created project configuration details.
    :rtype: ProjectConfigResponse
    """
    try:
        project_config = service.create_project_config(project_id, request.config)
        return ProjectConfigResponse(
            project_id=str(project_config.project_id),
            config={str(k): v for k, v in project_config.config.items()},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/projects/{project_id}/config', response_model=ProjectConfigResponse)
async def get_project_config(project_id: str, service: ProjectConfigService = Depends()):
    """
    Retrieve a project configuration by its project ID.

    :param project_id: The unique ID of the project.
    :type project_id: str
    :param service: The service used to handle project configuration-related operations.
    :type service: ProjectConfigService
    :return: The project configuration details.
    :rtype: ProjectConfigResponse
    :raises HTTPException: If the project configuration does not exist.
    """
    try:
        project_config = service.get_project_config(project_id)
        return ProjectConfigResponse(
            project_id=str(project_config.project_id),
            config={str(k): v for k, v in project_config.config.items()},
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project configuration not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/projects/{project_id}/config', response_model=ProjectConfigResponse)
async def update_project_config(project_id: str, request: ProjectConfigRequest, service: ProjectConfigService = Depends()):
    """
    Update an existing project configuration.

    :param project_id: The unique ID of the project.
    :type project_id: str
    :param request: The request body containing the configuration keys and values.
    :type request: ProjectConfigRequest
    :param service: The service used to handle project configuration-related operations.
    :type service: ProjectConfigService
    :return: The updated project configuration details.
    :rtype: ProjectConfigResponse
    :raises HTTPException: If the project configuration does not exist.
    """
    try:
        project_config = service.update_project_config(project_id, request.config)
        return ProjectConfigResponse(
            project_id=str(project_config.project_id),
            config={str(k): v for k, v in project_config.config.items()},
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project configuration not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/projects/{project_id}/config', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_config(project_id: str, service: ProjectConfigService = Depends()):
    """
    Delete a project configuration by its project ID.

    :param project_id: The unique ID of the project.
    :type project_id: str
    :param service: The service used to handle project configuration-related operations.
    :type service: ProjectConfigService
    :raises HTTPException: If the project configuration does not exist.
    """
    try:
        service.delete_project_config(project_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project configuration not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
