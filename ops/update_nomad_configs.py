#!/usr/bin/env python
"""
Update Nomad job files from client registry.

This script reads the CLIENT_REGISTRY and generates Nomad .hcl files
for all registered clients and their tasks, ensuring consistency between
code and deployment configs.

Usage:
    PYTHONPATH=src python ops/update_nomad_configs.py

This will:
1. Read all clients from CLIENT_REGISTRY
2. For each client and enabled task, generate train.hcl and predict.hcl files
3. Save them to ops/nomad/<client_name>/
"""

import os
import sys
from pathlib import Path

# Add src to path to import configs
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from clients import CLIENT_REGISTRY
from clients.base import NomadTaskConfig
from ml.tasks import TASK_CONFIG_REGISTRY

# Default configuration values
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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")
DEFAULT_TRAIN_CRON = "0 4 * * *"  # Daily at 4am UTC
DEFAULT_PREDICT_CRON = "0 */4 * * *"  # Every 4 hours
DEFAULT_MEMORY_MB = 1024
DEFAULT_ENV = "production"

# Templates directory
TEMPLATE_DIR = Path(__file__).parent / "nomad" / "_template"
OUTPUT_DIR = Path(__file__).parent / "nomad"


def load_template(template_name: str) -> str:
    """Load a Nomad template file."""
    template_path = TEMPLATE_DIR / template_name
    with open(template_path, "r") as f:
        return f.read()


def generate_nomad_config(
    template: str,
    client_name: str,
    config_registry_key: str,
    task_folder_name: str,
    db_user: str,
    db_password: str,
    cron_schedule: str,
    memory_mb: int,
    job_type: str,  # "train" or "predict"
) -> str:
    """Generate Nomad config from template by replacing placeholders.

    Args:
        config_registry_key: The registry key used to lookup the config (for job name, CLI param)
        task_folder_name: The actual folder name where train.py/predict.py lives (from config.task_name)
    """
    return (
        template.replace("{CLIENT_NAME}", client_name)
        .replace("{CONFIG_REGISTRY_KEY}", config_registry_key)
        .replace("{TASK_FOLDER_NAME}", task_folder_name)
        .replace("{DB_USER}", db_user)
        .replace("{DB_PASSWORD}", db_password)
        .replace("{CRON_SCHEDULE}", cron_schedule)
        .replace("{GITHUB_TOKEN}", GITHUB_TOKEN)
        .replace("{MEMORY_MB}", str(memory_mb))
        .replace("{JOB_TYPE}", job_type)
    )


def create_task_configs(
    client_name: str,
    db_user: str,
    db_password: str,
    config_registry_key: str,
    task_config: NomadTaskConfig,
) -> None:
    """Create Nomad config files for a client task.

    Args:
        config_registry_key: Key used in TASK_CONFIG_REGISTRY (e.g., "advanced_power_forecast_custom1")
        task_config: NomadTaskConfig from client
    """

    # Skip if task is disabled
    if not task_config.enabled:
        print(f"  ⊘ Skipping disabled task '{config_registry_key}'")
        return

    # Lookup the actual task config to get the folder name
    if config_registry_key not in TASK_CONFIG_REGISTRY:
        print(f"  ❌ Config '{config_registry_key}' not found in TASK_CONFIG_REGISTRY")
        return

    task_config_obj = TASK_CONFIG_REGISTRY[config_registry_key]
    task_folder_name = task_config_obj.task_name  # The actual folder name

    client_dir = OUTPUT_DIR / client_name
    client_dir.mkdir(parents=True, exist_ok=True)

    # Load templates
    train_template = load_template("train.hcl.template")
    predict_template = load_template("predict.hcl.template")

    # Get cron schedules (use defaults if not specified)
    train_cron = task_config.train_cron or DEFAULT_TRAIN_CRON
    predict_cron = task_config.predict_cron or DEFAULT_PREDICT_CRON
    memory_mb = task_config.memory_mb

    # Generate train config
    train_config = generate_nomad_config(
        train_template,
        client_name=client_name,
        config_registry_key=config_registry_key,
        task_folder_name=task_folder_name,
        db_user=db_user,
        db_password=db_password,
        cron_schedule=train_cron,
        memory_mb=memory_mb,
        job_type="train",
    )

    # Generate predict config
    predict_config = generate_nomad_config(
        predict_template,
        client_name=client_name,
        config_registry_key=config_registry_key,
        task_folder_name=task_folder_name,
        db_user=db_user,
        db_password=db_password,
        cron_schedule=predict_cron,
        memory_mb=memory_mb,
        job_type="predict",
    )

    # Write files (use registry key for filename)
    train_file = client_dir / f"{config_registry_key}-train.hcl"
    predict_file = client_dir / f"{config_registry_key}-predict.hcl"

    with open(train_file, "w") as f:
        f.write(train_config)

    with open(predict_file, "w") as f:
        f.write(predict_config)

    print(f"  ✓ {config_registry_key}")
    print(f"    - {train_file.name} (cron: {train_cron})")
    print(f"    - {predict_file.name} (cron: {predict_cron})")
    print(f"    → Task folder: src/ml/tasks/{task_folder_name}/")


def main():
    """Generate Nomad configs for all clients in the registry."""
    print("=" * 60)
    print("Updating Nomad configs from CLIENT_REGISTRY")
    print("=" * 60)

    if not CLIENT_REGISTRY:
        print("❌ No clients found in CLIENT_REGISTRY")
        sys.exit(1)

    total_tasks = 0

    for client_name, client_config in CLIENT_REGISTRY.items():
        print(f"\n📦 Client: {client_name}")

        if not client_config.tasks:
            print("  ⚠️  No tasks configured for this client")
            continue

        for task_name, task_config in client_config.tasks.items():
            try:
                create_task_configs(
                    client_name=client_config.client_name,
                    db_user=client_config.db_user,
                    db_password=client_config.db_password,
                    config_registry_key=task_name,  # This is the registry key
                    task_config=task_config,
                )
                if task_config.enabled:
                    total_tasks += 1
            except Exception as e:
                print(f"  ❌ Error generating configs for '{task_name}': {e}")
                continue

    print("\n" + "=" * 60)
    print("✅ Successfully updated Nomad configs")
    print(f"   Clients: {len(CLIENT_REGISTRY)}")
    print(f"   Tasks: {total_tasks}")
    print("=" * 60)
    print("\nNOTE: Review generated files before deploying to production.")


if __name__ == "__main__":
    main()
