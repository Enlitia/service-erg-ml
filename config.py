"""ERG Client Configuration."""

from pydantic_settings import BaseSettings


class ClientConfig(BaseSettings):
    """ERG-specific configuration."""

    # Client Identity
    client_name: str = "erg"

    # Database Configuration (credentials only, infrastructure settings in core-ml-platform configs)
    db_name: str = "erg"
    db_user: str = "app_hub"
    db_password: str = "2PWcx7VbxCHtRJNwQe1IUovN"


# Singleton instance
config = ClientConfig()
