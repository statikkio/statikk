from __future__ import annotations

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to manage environment variables.

    Attributes:
        database_url (str): The URL for connecting to the database.
        jwt_secret_key (str): The secret key used for JWT authentication.
        jwt_algorithm (str): The algorithm used for JWT encoding/decoding, defaults to HS256.
    """
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'


settings = Settings()
