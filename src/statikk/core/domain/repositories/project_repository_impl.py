# infrastructure/database/project_repository_impl.py
from typing import List
from statikk.core.domain.entities.project import Project
from statikk.core.domain.repositories.project_repository import ProjectRepository
from statikk.core.domain.value_objects.project_id import ProjectID
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient


class SubrrrealDBProjectRepository(ProjectRepository):
    """
    Implementation of ProjectRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, project_id: ProjectID) -> Project:
        """
        Retrieve a project by its unique identifier.

        :param project_id: The unique ID of the project.
        :type project_id: ProjectID
        :return: The project associated with the given ID.
        :rtype: Project
        :raises KeyError: If the project does not exist.
        :raises Exception: If a database error occurs.
        """
        try:
            query = f"SELECT * FROM projects WHERE id = '{project_id}'"
            result = self.db_client.query(query)
            if not result:
                raise KeyError(f"Project with ID {project_id} not found.")
            return Project(
                project_id=ProjectID(result['id']),
                name=result['name'],
                description=result['description']
            )
        except KeyError as e:
            # Specific handling if the project is not found
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            # General error handling for database errors
            print(f"Failed to retrieve project: {str(e)}")
            raise Exception(f"Database error: Could not retrieve project with ID {project_id}.") from e

    def save(self, project: Project) -> None:
        """
        Save a project entity to the database.

        :param project: The project entity to save.
        :type project: Project
        :raises Exception: If a database error occurs.
        """
        try:
            self.db_client.insert(
                collection="projects",
                data={
                    "id": str(project.project_id),
                    "name": project.name,
                    "description": project.description
                }
            )
            print(f"Project {project.name} saved successfully.")
        except Exception as e:
            print(f"Failed to save project: {str(e)}")
            raise Exception(f"Database error: Could not save project {project.name}.") from e

    def update(self, project: Project) -> None:
        """
        Update an existing project entity in the database.

        :param project: The project entity to update.
        :type project: Project
        :raises KeyError: If the project does not exist.
        :raises Exception: If a database error occurs.
        """
        try:
            # Check if the project exists before updating
            existing_project = self.get_by_id(project.project_id)
            if not existing_project:
                raise KeyError(f"Project with ID {project.project_id} not found for update.")

            self.db_client.update(
                collection="projects",
                identifier=str(project.project_id),
                data={
                    "name": project.name,
                    "description": project.description
                }
            )
            print(f"Project {project.name} updated successfully.")
        except KeyError as e:
            # Specific handling if the project to update is not found
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            # General error handling for database errors
            print(f"Failed to update project: {str(e)}")
            raise Exception(f"Database error: Could not update project with ID {project.project_id}.") from e

    def delete(self, project_id: ProjectID) -> None:
        """
        Delete a project by its unique identifier.

        :param project_id: The unique ID of the project to delete.
        :type project_id: ProjectID
        :raises KeyError: If the project does not exist.
        :raises Exception: If a database error occurs.
        """
        try:
            # Check if the project exists before deleting
            existing_project = self.get_by_id(project_id)
            if not existing_project:
                raise KeyError(f"Project with ID {project_id} not found for deletion.")

            self.db_client.delete(
                collection="projects",
                identifier=str(project_id)
            )
            print(f"Project with ID {project_id} deleted successfully.")
        except KeyError as e:
            # Specific handling if the project to delete is not found
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            # General error handling for database errors
            print(f"Failed to delete project: {str(e)}")
            raise Exception(f"Database error: Could not delete project with ID {project_id}.") from e
