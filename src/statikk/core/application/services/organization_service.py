from statikk.core.domain.entities.organization import Organization
from statikk.core.domain.entities.role import Role
from statikk.core.domain.value_objects.permissions import Permission
from statikk.core.domain.repositories.organization_repository import OrganizationRepository
from statikk.core.domain.value_objects.organization_id import OrganizationID
from statikk.core.domain.value_objects.user_id import UserID
from statikk.core.domain.value_objects.role_id import RoleID
from typing import Dict, List

class OrganizationService:
    """
    Service for handling organization-related operations with RBAC features.

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

    def update_organization(self, organization_id: str, name: str, requesting_user_id: str) -> Organization:
        """
        Update an existing organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param name: The new name of the organization.
        :type name: str
        :param requesting_user_id: The UserID of the user making the request.
        :type requesting_user_id: str
        :return: The updated Organization object.
        :rtype: Organization
        :raises KeyError: If the organization does not exist.
        :raises PermissionError: If the requesting user does not have permission to update the organization.
        """
        organization = self.get_organization(organization_id)
        if not self.check_permission(organization_id, requesting_user_id, Permission("update_organization")):
            raise PermissionError("User does not have permission to update the organization.")

        organization.name = name
        self.organization_repository.update(organization)
        return organization

    def delete_organization(self, organization_id: str, requesting_user_id: str) -> None:
        """
        Delete an organization by its unique identifier.

        :param organization_id: The unique ID of the organization to delete.
        :type organization_id: str
        :param requesting_user_id: The UserID of the user making the request.
        :type requesting_user_id: str
        :raises KeyError: If the organization does not exist.
        :raises PermissionError: If the requesting user does not have permission to delete the organization.
        """
        if not self.check_permission(organization_id, requesting_user_id, Permission("delete_organization")):
            raise PermissionError("User does not have permission to delete the organization.")
        self.organization_repository.delete(OrganizationID(organization_id))

    def add_member(self, organization_id: str, user_id: str, role: Role, requesting_user_id: str) -> Organization:
        """
        Add a member to the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member to add.
        :type user_id: str
        :param role: The role of the member within the organization.
        :type role: Role
        :param requesting_user_id: The UserID of the user making the request.
        :type requesting_user_id: str
        :return: The updated Organization object.
        :rtype: Organization
        :raises PermissionError: If the requesting user does not have permission to add members.
        """
        organization = self.get_organization(organization_id)
        if not self.check_permission(organization_id, requesting_user_id, Permission("add_member")):
            raise PermissionError("User does not have permission to add members to the organization.")

        organization.add_member(UserID(user_id), role)
        self.organization_repository.update(organization)
        return organization

    def remove_member(self, organization_id: str, user_id: str, requesting_user_id: str) -> Organization:
        """
        Remove a member from the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member to remove.
        :type user_id: str
        :param requesting_user_id: The UserID of the user making the request.
        :type requesting_user_id: str
        :return: The updated Organization object.
        :rtype: Organization
        :raises PermissionError: If the requesting user does not have permission to remove members.
        """
        organization = self.get_organization(organization_id)
        if not self.check_permission(organization_id, requesting_user_id, Permission("remove_member")):
            raise PermissionError("User does not have permission to remove members from the organization.")

        organization.remove_member(UserID(user_id))
        self.organization_repository.update(organization)
        return organization

    def update_member_role(self, organization_id: str, user_id: str, new_role: Role, requesting_user_id: str) -> Organization:
        """
        Update the role of a member within the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member whose role is to be updated.
        :type user_id: str
        :param new_role: The new role for the member.
        :type new_role: Role
        :param requesting_user_id: The UserID of the user making the request.
        :type requesting_user_id: str
        :return: The updated Organization object.
        :rtype: Organization
        :raises PermissionError: If the requesting user does not have permission to update member roles.
        """
        organization = self.get_organization(organization_id)
        if not self.check_permission(organization_id, requesting_user_id, Permission("update_member_role")):
            raise PermissionError("User does not have permission to update member roles.")

        organization.update_member_role(UserID(user_id), new_role)
        self.organization_repository.update(organization)
        return organization

    def check_permission(self, organization_id: str, user_id: str, permission: Permission) -> bool:
        """
        Check if a member has the specified permission within the organization.

        :param organization_id: The unique ID of the organization.
        :type organization_id: str
        :param user_id: The UserID of the member.
        :type user_id: str
        :param permission: The permission to check.
        :type permission: Permission
        :return: True if the member has the permission, otherwise False.
        :rtype: bool
        """
        organization = self.get_organization(organization_id)
        role = organization.get_member_role(UserID(user_id))
        return role.has_permission(permission) if role else False
