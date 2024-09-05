from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.role import Role
from statikk.core.domain.value_objects.role_id import RoleID


class RoleRepository(ABC):
    """
    Interface for the Role repository that defines methods to interact with Role data.
    """

    @abstractmethod
    def get_by_id(self, role_id: RoleID) -> Role:
        pass

    @abstractmethod
    def save(self, role: Role) -> None:
        pass

    @abstractmethod
    def update(self, role: Role) -> None:
        pass

    @abstractmethod
    def delete(self, role_id: RoleID) -> None:
        pass
