# infrastructure/database/organization_repository_impl.py
from __future__ import annotations

from statikk.core.domain.entities.organization import Organization
from statikk.core.domain.repositories.organization_repository import OrganizationRepository
from statikk.core.domain.value_objects.organization_id import OrganizationID
from statikk.core.domain.value_objects.user_id import UserID
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient


class SubrrrealDBOrganizationRepository(OrganizationRepository):
    """
    Implementation of OrganizationRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, organization_id: OrganizationID) -> Organization:
        """
        Retrieve an organization by its unique identifier.

        :param organization_id: The unique ID of the organization.
        :type organization_id: OrganizationID
        :return: The organization associated with the given ID.
        :rtype: Organization
        :raises KeyError: If the organization does not exist.
        """
        try:
            query = f"SELECT * FROM organizations WHERE id = '{organization_id}'"
            result = self.db_client.query(query)
            if not result:
                raise KeyError(f"Organization with ID {organization_id} not found.")
            return Organization(
                organization_id=OrganizationID(result['id']),
                name=result['name'],
                owner_id=UserID(result['owner_id']),
                members={UserID(k): v for k, v in result['members'].items()},
            )
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to retrieve organization: {str(e)}")
            raise Exception(f"Database error: Could not retrieve organization with ID {organization_id}.") from e

    def save(self, organization: Organization) -> None:
        """
        Save an organization entity to the database.

        :param organization: The organization entity to save.
        :type organization: Organization
        """
        try:
            self.db_client.insert(
                collection='organizations',
                data={
                    'id': str(organization.organization_id),
                    'name': organization.name,
                    'owner_id': str(organization.owner_id),
                    'members': {str(k): v for k, v in organization.members.items()},
                },
            )
            print(f"Organization {organization.name} saved successfully.")
        except Exception as e:
            print(f"Failed to save organization: {str(e)}")
            raise Exception(f"Database error: Could not save organization {organization.name}.") from e

    def update(self, organization: Organization) -> None:
        """
        Update an existing organization entity in the database.

        :param organization: The organization entity to update.
        :type organization: Organization
        """
        try:
            existing_org = self.get_by_id(organization.organization_id)
            if not existing_org:
                raise KeyError(f"Organization with ID {organization.organization_id} not found for update.")

            self.db_client.update(
                collection='organizations',
                identifier=str(organization.organization_id),
                data={
                    'name': organization.name,
                    'owner_id': str(organization.owner_id),
                    'members': {str(k): v for k, v in organization.members.items()},
                },
            )
            print(f"Organization {organization.name} updated successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to update organization: {str(e)}")
            raise Exception(f"Database error: Could not update organization with ID {organization.organization_id}.") from e

    def delete(self, organization_id: OrganizationID) -> None:
        """
        Delete an organization by its unique identifier.

        :param organization_id: The unique ID of the organization to delete.
        :type organization_id: OrganizationID
        """
        try:
            existing_org = self.get_by_id(organization_id)
            if not existing_org:
                raise KeyError(f"Organization with ID {organization_id} not found for deletion.")

            self.db_client.delete(
                collection='organizations',
                identifier=str(organization_id),
            )
            print(f"Organization with ID {organization_id} deleted successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to delete organization: {str(e)}")
            raise Exception(f"Database error: Could not delete organization with ID {organization_id}.") from e
