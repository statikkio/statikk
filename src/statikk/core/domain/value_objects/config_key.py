from __future__ import annotations


class ConfigKey:
    """
    Represents a configuration key for a ProjectConfig.

    :param key: The configuration key string.
    :type key: str
    """

    def __init__(self, key: str):
        self.key = key

    def __eq__(self, other):
        return isinstance(other, ConfigKey) and self.key == other.key

    def __str__(self):
        return self.key
