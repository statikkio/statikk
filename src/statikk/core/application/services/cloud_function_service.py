# core/application/services/cloud_function_service.py
from __future__ import annotations

from statikk.core.domain.entities.cloud_function import CloudFunction
from statikk.core.domain.repositories.cloud_function_repository import CloudFunctionRepository
from statikk.core.domain.value_objects.cloud_function_id import CloudFunctionID


class CloudFunctionService:
    """
    Service for handling cloud function-related operations.

    :param cloud_function_repository: Repository for interacting with cloud function data.
    :type cloud_function_repository: CloudFunctionRepository
    """

    def __init__(self, cloud_function_repository: CloudFunctionRepository):
        self.cloud_function_repository = cloud_function_repository

    def create_cloud_function(self, name: str, code: str, triggers: list[str]) -> CloudFunction:
        """
        Create a new cloud function.

        :param name: The name of the cloud function.
        :param code: The code of the cloud function.
        :param triggers: A list of triggers for the cloud function.
        :return: The created CloudFunction object.
        :rtype: CloudFunction
        """
        cloud_function = CloudFunction(
            function_id=CloudFunctionID(),
            name=name,
            code=code,
            triggers=triggers,
        )
        self.cloud_function_repository.save(cloud_function)
        return cloud_function

    def get_cloud_function(self, function_id: str) -> CloudFunction:
        """
        Retrieve a cloud function by its unique identifier.

        :param function_id: The unique ID of the cloud function.
        :type function_id: str
        :return: The cloud function associated with the given ID.
        :rtype: CloudFunction
        :raises KeyError: If the cloud function does not exist.
        """
        return self.cloud_function_repository.get_by_id(CloudFunctionID(function_id))

    def update_cloud_function(self, function_id: str, new_code: str, triggers: list[str]) -> CloudFunction:
        """
        Update an existing cloud function.

        :param function_id: The unique ID of the cloud function.
        :param new_code: The new code for the cloud function.
        :param triggers: Updated list of triggers for the cloud function.
        :return: The updated CloudFunction object.
        :rtype: CloudFunction
        :raises KeyError: If the cloud function does not exist.
        """
        cloud_function = self.get_cloud_function(function_id)
        cloud_function.update_code(new_code)
        cloud_function.triggers = triggers
        self.cloud_function_repository.update(cloud_function)
        return cloud_function

    def delete_cloud_function(self, function_id: str) -> None:
        """
        Delete a cloud function by its unique identifier.

        :param function_id: The unique ID of the cloud function to delete.
        :type function_id: str
        :raises KeyError: If the cloud function does not exist.
        """
        self.cloud_function_repository.delete(CloudFunctionID(function_id))

    def list_all_cloud_functions(self) -> list[CloudFunction]:
        """
        List all cloud functions.

        :return: A list of all cloud functions.
        :rtype: List[CloudFunction]
        """
        # Assuming list_all method exists in the repository
        return self.cloud_function_repository.list_all()
