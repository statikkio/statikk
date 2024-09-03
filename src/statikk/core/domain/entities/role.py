from statikk.core.domain.value_objects.role_id import RoleID
from statikk.core.domain.value_objects.permissions import Permission
from typing import List

class Role:
    """
    Represents a user role with specific permissions.

    :param role_id: Unique identifier for the role.
    :type role_id: RoleID
    :param name: The name of the role (e.g., "admin", "editor").
    :type name: str
    :param permissions: A list of permissions associated with the role.
    :type permissions: List[Permission]
    """

    def __init__(self, role_id: RoleID, name: str, permissions: List[Permission]):
        self.role_id = role_id
        self.name = name
        self.permissions = permissions

    def add_permission(self, permission: Permission):
        """
        Add a permission to the role.

        :param permission: The permission to add.
        :type permission: Permission
        """
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: Permission):
        """
        Remove a permission from the role.

        :param permission: The permission to remove.
        :type permission: Permission
        """
        if permission in self.permissions:
            self.permissions.remove(permission)

    def has_permission(self, permission: Permission) -> bool:
        """
        Check if the role has a specific permission.

        :param permission: The permission to check.
        :type permission: Permission
        :return: True if the role has the permission, otherwise False.
        :rtype: bool
        """
        return permission in self.permissions
