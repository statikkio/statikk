# core/domain/repositories/project_config_repository.py
from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.project_config import ProjectConfig
from statikk.core.domain.value_objects.project_id import ProjectID


class ProjectConfigRepository(ABC):
    """
    Interface for the ProjectConfig repository that defines methods to interact with ProjectConfig data.
    """

    @abstractmethod
    def get_by_project_id(self, project_id: ProjectID) -> ProjectConfig:
        pass

    @abstractmethod
    def save(self, project_config: ProjectConfig) -> None:
        pass

    @abstractmethod
    def update(self, project_config: ProjectConfig) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: ProjectID) -> None:
        pass
