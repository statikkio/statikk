from statikk.core.domain.entities.project import Project
from statikk.core.domain.repositories.project_repository import ProjectRepository
from statikk.core.domain.value_objects.project_id import ProjectID

class ProjectService:
    """
    Service for handling project-related operations.

    :param project_repository: Repository for interacting with project data.
    :type project_repository: ProjectRepository
    """

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project.

        :param name: The name of the project.
        :param description: A description of the project.
        :return: The created Project object.
        """
        project = Project(project_id=ProjectID(), name=name, description=description)
        self.project_repository.save(project)
        return project
