# tests/unit/test_project_service.py
from __future__ import annotations

from unittest.mock import Mock

import pytest
from statikk.core.application.services.project_service import ProjectService
from statikk.core.domain.entities.project import Project
from statikk.core.domain.repositories.project_repository import ProjectRepository
from statikk.core.domain.value_objects.project_id import ProjectID


@pytest.fixture
def mock_project_repository():
    return Mock(spec=ProjectRepository)


@pytest.fixture
def project_service(mock_project_repository):
    return ProjectService(project_repository=mock_project_repository)


def test_create_project(project_service, mock_project_repository):
    # Arrange
    name = 'Test Project'
    description = 'Description of the test project'
    expected_project = Project(project_id=ProjectID(), name=name, description=description)

    # Act
    project = project_service.create_project(name, description)

    # Assert
    assert project.name == expected_project.name
    assert project.description == expected_project.description
    mock_project_repository.save.assert_called_once_with(project)
