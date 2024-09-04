# core/application/services/project_config_service.py
from __future__ import annotations

from statikk.core.domain.entities.project_config import ProjectConfig
from statikk.core.domain.repositories.project_config_repository import ProjectConfigRepository
from statikk.core.domain.value_objects.config_key import ConfigKey
from statikk.core.domain.value_objects.project_id import ProjectID


class ProjectConfigService:
    """
    Service for handling project configuration-related operations.

    :param project_config_repository: Repository for interacting with project configuration data.
    :type project_config_repository: ProjectConfigRepository
    """

    def __init__(self, project_config_repository: ProjectConfigRepository):
        self.project_config_repository = project_config_repository

    def create_project_config(self, project_id: str, config: dict) -> ProjectConfig:
        """
        Create a new project configuration.

        :param project_id: The unique ID of the project.
        :type project_id: str
        :param config: A dictionary containing configuration keys and values.
        :type config: dict
        :return: The created ProjectConfig object.
        :rtype: ProjectConfig
        """
        project_config = ProjectConfig(
            project_id=ProjectID(project_id),
            config={ConfigKey(k): v for k, v in config.items()},
        )
        self.project_config_repository.save(project_config)
        return project_config

    def get_project_config(self, project_id: str) -> ProjectConfig:
        """
        Retrieve a project configuration by its project ID.

        :param project_id: The unique ID of the project.
        :type project_id: str
        :return: The ProjectConfig associated with the given project ID.
        :rtype: ProjectConfig
        :raises KeyError: If the project configuration does not exist.
        """
        return self.project_config_repository.get_by_project_id(ProjectID(project_id))

    def update_project_config(self, project_id: str, config: dict) -> ProjectConfig:
        """
        Update an existing project configuration.

        :param project_id: The unique ID of the project.
        :type project_id: str
        :param config: A dictionary containing configuration keys and values.
        :type config: dict
        :return: The updated ProjectConfig object.
        :rtype: ProjectConfig
        :raises KeyError: If the project configuration does not exist.
        """
        project_config = self.get_project_config(project_id)
        for key, value in config.items():
            project_config.update_config(ConfigKey(key), value)
        self.project_config_repository.update(project_config)
        return project_config

    def delete_project_config(self, project_id: str) -> None:
        """
        Delete a project configuration by its project ID.

        :param project_id: The unique ID of the project.
        :type project_id: str
        :raises KeyError: If the project configuration does not exist.
        """
        self.project_config_repository.delete(ProjectID(project_id))
