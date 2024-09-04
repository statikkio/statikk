from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.organization import Organization
from statikk.core.domain.value_objects.organization_id import OrganizationID


class OrganizationRepository(ABC):
    """
    Interface for the Organization repository that defines methods to interact with Organization data.
    """

    @abstractmethod
    def get_by_id(self, organization_id: OrganizationID) -> Organization:
        pass

    @abstractmethod
    def save(self, organization: Organization) -> None:
        pass

    @abstractmethod
    def update(self, organization: Organization) -> None:
        pass

    @abstractmethod
    def delete(self, organization_id: OrganizationID) -> None:
        pass
