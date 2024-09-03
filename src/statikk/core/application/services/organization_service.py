from statikk.core.domain.entities.organization import Organization
from statikk.core.domain.repositories.organization_repository import OrganizationRepository
from statikk.core.domain.value_objects.organization_id import OrganizationID
from statikk.core.domain.value_objects.user_id import UserID
from typing import Dict

class OrganizationService:
    """
    Service for handling organization-related operations.

    :param organization_repository: Repository for interacting with organization data.
    :type organization_repository: OrganizationRepository
    """

    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    def create_organization(self, name: str, owner_id: str) -> Organization:
        """
        Create a new organization.

        :param name: The name of the organization.
        :type name: str
        :param owner_id: The UserID of the organization's owner.
        :type owner_id: str
        :return: The created Organization object.
        :rtype: Organization
        """
        organization = Organization(
            organization_id=OrganizationID(),
            name=name,
            owner_id=UserID(owner_id)
        )
        self.organization_repository.save(organization)
        return organization

    def get_organization(self, organization_id: str) -> Organization:
        """
        Retrieve an organization by its unique identifier.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :return: The organization associated with the given ID.
        :rtype: Organization
        :raises KeyError: If the organization does not exist.
        """
        return self.organization_repository.get_by_id(OrganizationID(organization_id))

    def update_organization(self, organization_id: str, name: str) -> Organization:
        """
        Update an existing organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param name: The new name of the organization.
        :type name: str
        :return: The updated Organization object.
        :rtype: Organization
        :raises KeyError: If the organization does not exist.
        """
        organization = self.get_organization(organization_id)
        organization.name = name
        self.organization_repository.update(organization)
        return organization

    def delete_organization(self, organization_id: str) -> None:
        """
        Delete an organization by its unique identifier.

        :param organization_id: The unique ID of the organization to delete.
        :type organization_id: str
        :raises KeyError: If the organization does not exist.
        """
        self.organization_repository.delete(OrganizationID(organization_id))

    def add_member(self, organization_id: str, user_id: str, role: str) -> Organization:
        """
        Add a member to the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member to add.
        :type user_id: str
        :param role: The role of the member within the organization.
        :type role: str
        :return: The updated Organization object.
        :rtype: Organization
        """
        organization = self.get_organization(organization_id)
        organization.add_member(UserID(user_id), role)
        self.organization_repository.update(organization)
        return organization

    def remove_member(self, organization_id: str, user_id: str) -> Organization:
        """
        Remove a member from the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member to remove.
        :type user_id: str
        :return: The updated Organization object.
        :rtype: Organization
        """
        organization = self.get_organization(organization_id)
        organization.remove_member(UserID(user_id))
        self.organization_repository.update(organization)
        return organization

    def update_member_role(self, organization_id: str, user_id: str, new_role: str) -> Organization:
        """
        Update the role of a member within the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member whose role is to be updated.
        :type user_id: str
        :param new_role: The new role for the member.
        :type new_role: str
        :return: The updated Organization object.
        :rtype: Organization
        """
        organization = self.get_organization(organization_id)
        organization.update_member_role(UserID(user_id), new_role)
        self.organization_repository.update(organization)
        return organization
