from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from statikk.core.application.services.project_service import ProjectService

router = APIRouter()

# Pydantic model for project response


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str


@router.get('/projects', response_model=list[ProjectResponse])
async def list_projects(project_service: ProjectService = Depends()):
    """
    Endpoint to list all projects.

    :param project_service: Service for handling project operations.
    :type project_service: ProjectService
    :return: A list of all projects.
    :rtype: List[ProjectResponse]
    """
    projects = project_service.list_all_projects()
    return [ProjectResponse(project_id=str(p.project_id), name=p.name, description=p.description) for p in projects]
