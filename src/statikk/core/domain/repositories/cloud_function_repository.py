from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from statikk.core.domain.entities.cloud_function import CloudFunction
from statikk.core.domain.value_objects.cloud_function_id import CloudFunctionID


class CloudFunctionRepository(ABC):
    """
    Interface for the CloudFunction repository that defines methods to interact with CloudFunction data.
    """

    @abstractmethod
    def get_by_id(self, function_id: CloudFunctionID) -> CloudFunction:
        pass

    @abstractmethod
    def save(self, cloud_function: CloudFunction) -> None:
        pass

    @abstractmethod
    def update(self, cloud_function: CloudFunction) -> None:
        pass

    @abstractmethod
    def delete(self, function_id: CloudFunctionID) -> None:

        pass

    @abstractmethod
    def list_all(self) -> list[CloudFunction]:
        pass
