# infrastructure/database/cloud_function_repository_impl.py
from __future__ import annotations

from statikk.core.domain.entities.cloud_function import CloudFunction
from statikk.core.domain.repositories.cloud_function_repository import CloudFunctionRepository
from statikk.core.domain.value_objects.cloud_function_id import CloudFunctionID
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient


class SubrrrealDBCloudFunctionRepository(CloudFunctionRepository):
    """
    Implementation of CloudFunctionRepository using SubrrrealDB.

    :param db_client: The SubrrrealDB client.
    :type db_client: SubrrrealDBClient
    """

    def __init__(self, db_client: SubrrealDBClient):
        self.db_client = db_client

    def get_by_id(self, function_id: CloudFunctionID) -> CloudFunction:
        """
        Retrieve a cloud function by its unique identifier.

        :param function_id: The unique ID of the cloud function.
        :type function_id: CloudFunctionID
        :return: The cloud function associated with the given ID.
        :rtype: CloudFunction
        :raises KeyError: If the cloud function does not exist.
        """
        try:
            query = f"SELECT * FROM cloud_functions WHERE id = '{function_id}'"
            result = self.db_client.query(query)
            if not result:
                raise KeyError(f"Cloud function with ID {function_id} not found.")
            return CloudFunction(
                function_id=CloudFunctionID(result['id']),
                name=result['name'],
                code=result['code'],
                triggers=result['triggers'],
            )
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to retrieve cloud function: {str(e)}")
            raise Exception(f"Database error: Could not retrieve cloud function with ID {function_id}.") from e

    def save(self, cloud_function: CloudFunction) -> None:
        """
        Save a cloud function entity to the database.

        :param cloud_function: The cloud function entity to save.
        :type cloud_function: CloudFunction
        """
        try:
            self.db_client.insert(
                collection='cloud_functions',
                data={
                    'id': str(cloud_function.function_id),
                    'name': cloud_function.name,
                    'code': cloud_function.code,
                    'triggers': cloud_function.triggers,
                },
            )
            print(f"Cloud function {cloud_function.name} saved successfully.")
        except Exception as e:
            print(f"Failed to save cloud function: {str(e)}")
            raise Exception(f"Database error: Could not save cloud function {cloud_function.name}.") from e

    def update(self, cloud_function: CloudFunction) -> None:
        """
        Update an existing cloud function entity in the database.

        :param cloud_function: The cloud function entity to update.
        :type cloud_function: CloudFunction
        """
        try:
            existing_function = self.get_by_id(cloud_function.function_id)
            if not existing_function:
                raise KeyError(f"Cloud function with ID {cloud_function.function_id} not found for update.")

            self.db_client.update(
                collection='cloud_functions',
                identifier=str(cloud_function.function_id),
                data={
                    'name': cloud_function.name,
                    'code': cloud_function.code,
                    'triggers': cloud_function.triggers,
                },
            )
            print(f"Cloud function {cloud_function.name} updated successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to update cloud function: {str(e)}")
            raise Exception(f"Database error: Could not update cloud function with ID {cloud_function.function_id}.") from e

    def delete(self, function_id: CloudFunctionID) -> None:
        """
        Delete a cloud function by its unique identifier.

        :param function_id: The unique ID of the cloud function to delete.
        :type function_id: CloudFunctionID
        """
        try:
            existing_function = self.get_by_id(function_id)
            if not existing_function:
                raise KeyError(f"Cloud function with ID {function_id} not found for deletion.")

            self.db_client.delete(
                collection='cloud_functions',
                identifier=str(function_id),
            )
            print(f"Cloud function with ID {function_id} deleted successfully.")
        except KeyError as e:
            print(f"Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"Failed to delete cloud function: {str(e)}")
            raise Exception(f"Database error: Could not delete cloud function with ID {function_id}.") from e

    def list_all(self) -> list[CloudFunction]:
        """
        List all cloud functions in the database.

        :return: A list of all cloud functions.
        :rtype: List[CloudFunction]
        """
        try:
            results = self.db_client.query('SELECT * FROM cloud_functions')
            cloud_functions = [
                CloudFunction(
                    function_id=CloudFunctionID(result['id']),
                    name=result['name'],
                    code=result['code'],
                    triggers=result['triggers'],
                )
                for result in results
            ]
            return cloud_functions
        except Exception as e:
            print(f"Failed to list cloud functions: {str(e)}")
            raise Exception('Database error: Could not list cloud functions.') from e
