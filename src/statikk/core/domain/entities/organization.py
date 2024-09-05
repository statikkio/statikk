from __future__ import annotations

from statikk.core.domain.entities.role import Role
from statikk.core.domain.value_objects.organization_id import OrganizationID
from statikk.core.domain.value_objects.user_id import UserID


class Organization:
    """
    Represents an organization that can own resources like collections, cloud functions, etc.

    :param organization_id: Unique identifier for the organization.
    :type organization_id: OrganizationID
    :param name: The name of the organization.
    :type name: str
    :param owner_id: The UserID of the organization's owner.
    :type owner_id: UserID
    :param members: A dictionary of members and their roles within the organization.
    :type members: Dict[UserID, Role]
    """

    def __init__(self, organization_id: OrganizationID, name: str, owner_id: UserID, members: dict[str, Role] | None = None):
        self.organization_id = organization_id
        self.name = name
        self.owner_id = owner_id
        self.members = members or {}

    def add_member(self, user_id: UserID, role: Role):
        """
        Add a member to the organization with a specified role.

        :param user_id: The UserID of the member to add.
        :type user_id: UserID
        :param role: The role of the member within the organization.
        :type role: Role
        """
        self.members[user_id.id] = role

    def remove_member(self, user_id: UserID):
        """
        Remove a member from the organization.

        :param user_id: The UserID of the member to remove.
        :type user_id: UserID
        """
        print(self.members)
        if user_id.id in self.members:
            del self.members[user_id.id]

    def update_member_role(self, user_id: UserID, new_role: Role):
        """
        Update the role of a member within the organization.

        :param user_id: The UserID of the member whose role is to be updated.
        :type user_id: UserID
        :param new_role: The new role for the member.
        :type new_role: Role
        """
        if user_id.id in self.members:
            self.members[user_id.id] = new_role

    def get_member_role(self, user_id: UserID) -> Role | None:
        """
        Get the role of a member within the organization.

        :param user_id: The UserID of the member.
        :type user_id: UserID
        :return: The role of the member.
        :rtype: Role
        """
        return self.members.get(user_id.id)
