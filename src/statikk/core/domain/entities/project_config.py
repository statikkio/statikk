from __future__ import annotations

from statikk.core.domain.value_objects.config_key import ConfigKey
from statikk.core.domain.value_objects.project_id import ProjectID


class ProjectConfig:
    """
    Represents a configuration for a project.

    :param project_id: Unique identifier for the project.
    :type project_id: ProjectID
    :param config: A dictionary containing configuration keys and their values.
    :type config: Dict[ConfigKey, str]
    """

    def __init__(self, project_id: ProjectID, config: dict[ConfigKey, str] | None = None):
        self.project_id = project_id
        self.config = config or {}

    def add_config(self, key: ConfigKey, value: str):
        """
        Add a configuration key-value pair to the project configuration.

        :param key: The configuration key.
        :type key: ConfigKey
        :param value: The value for the configuration key.
        :type value: str
        """
        self.config[key] = value

    def update_config(self, key: ConfigKey, value: str):
        """
        Update an existing configuration key-value pair.

        :param key: The configuration key.
        :type key: ConfigKey
        :param value: The new value for the configuration key.
        :type value: str
        """
        self.config[key] = value

    def remove_config(self, key: ConfigKey):
        """
        Remove a configuration key from the project configuration.

        :param key: The configuration key to remove.
        :type key: ConfigKey
        """
        if key in self.config:
            del self.config[key]
