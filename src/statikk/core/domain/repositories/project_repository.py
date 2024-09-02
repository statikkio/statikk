from abc import ABC, abstractmethod
from statikk.core.domain.entities.project import Project
from statikk.core.domain.value_objects.project_id import ProjectID

class ProjectRepository(ABC):
    """
    Interface for the Project repository that defines methods to interact with Project data.
    """

    @abstractmethod
    def get_by_id(self, project_id: ProjectID) -> Project:
        """
        Retrieve a project by its unique identifier.

        :param project_id: The unique ID of the project.
        :type project_id: ProjectID
        :return: The project associated with the given ID.
        :rtype: Project
        :raises KeyError: If the project does not exist.
        """
        pass

    @abstractmethod
    def save(self, project: Project) -> None:
        """
        Save a project entity to the repository.

        :param project: The project entity to save.
        :type project: Project
        """
        pass

    @abstractmethod
    def update(self, project: Project) -> None:
        """
        Update an existing project entity in the repository.

        :param project: The project entity to update.
        :type project: Project
        """
        pass

    @abstractmethod
    def delete(self, project_id: ProjectID) -> None:
        """
        Delete a project by its unique identifier.

        :param project_id: The unique ID of the project to delete.
        :type project_id: ProjectID
        """
        pass
