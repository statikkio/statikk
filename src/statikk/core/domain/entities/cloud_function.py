from __future__ import annotations

from statikk.core.domain.value_objects import CloudFunctionID


class CloudFunction:
    """
    Represents a serverless function in the system.

    :param function_id: Unique identifier for the cloud function.
    :type function_id: CloudFunctionID
    :param name: The name of the cloud function.
    :type name: str
    :param code: The code of the cloud function, typically in a string format.
    :type code: str
    :param triggers: The events that trigger the function (e.g., HTTP request, data change).
    :type triggers: list
    """

    def __init__(self, function_id: CloudFunctionID, name: str, code: str, triggers: list):
        self.function_id = function_id
        self.name = name
        self.code = code
        self.triggers = triggers

    def update_code(self, new_code: str):
        """
        Update the code of the cloud function.

        :param new_code: The new code for the function.
        :type new_code: str
        """
        self.code = new_code

    def add_trigger(self, trigger: str):
        """
        Add a trigger to the cloud function.

        :param trigger: The event that will trigger the function.
        :type trigger: str
        """
        self.triggers.append(trigger)
