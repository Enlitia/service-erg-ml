"""ERG Client Configuration."""

import os
from pydantic_settings import BaseSettings


class ClientConfig(BaseSettings):
    """ERG-specific configuration."""

    # Client Identity
    client_name: str = "erg"

    # Database Configuration
    db_name: str = "erg"
    db_user: str = os.getenv("DB_USER", "app_hub")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = "192.168.60.18"
    db_port: int = 5432

    # Task Configuration - Which tasks ERG uses
    enabled_tasks: list[str] = [
        "advanced_power_forecast",
    ]

    # Nomad Configuration for each task
    nomad_configs: dict[str, dict] = {
        "advanced_power_forecast": {
            "train_cron": "0 4 * * *",  # Daily at 4am
            "predict_cron": "0 */4 * * *",  # Every 4 hours
            "memory_mb": 1024,
            "enabled": True,
        },
    }

    # MLflow Configuration
    mlflow_tracking_uri: str = "/app/mlruns/erg"

    # Loki Logging (optional)
    loki_url: str = os.getenv("LOKI_URL", "")


# Singleton instance
config = ClientConfig()
