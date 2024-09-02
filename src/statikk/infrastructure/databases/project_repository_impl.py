from statikk.core.domain.entities.project import Project
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient

class SubrrrealDBProjectRepository(ProjectRepository):
    """
    Implementation of ProjectRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, project_id: str) -> Project:
        """
        Retrieve a project by its unique identifier.

        :param project_id: The unique ID of the project.
        :type project_id: str
        :return: The project associated with the given ID.
        :rtype: Project
        """
        # Implement retrieval logic from SubrrrealDB
        data = self.db_client.query(f"SELECT * FROM projects WHERE id = {project_id}")
        return Project(project_id=data['id'], name=data['name'], description=data['description'])

    def save(self, project: Project) -> None:
        """
        Save a project entity to the database.

        :param project: The project entity to save.
        :type project: Project
        """
        # Implement save logic to SubrrrealDB
        self.db_client.insert("projects", {"id": project.project_id.id, "name": project.name, "description": project.description})
