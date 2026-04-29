# Service ERG ML

ERG client deployment for the Core ML Platform.

## Overview

This repository contains only configuration and deployment files for the ERG client. All ML logic resides in the `core-ml-platform` submodule.

## Repository Structure

```
service-erg-ml/
├── core-ml-platform/          # Git submodule - the complete ML framework
├── config.py                  # ERG-specific configuration
├── Dockerfile                 # Builds ERG container with framework
├── .env.example               # Environment variables template
└── README.md
```

## Quick Start

### 1. Clone with Submodule

```bash
git clone --recursive https://github.com/enlitia/service-erg-ml.git
cd service-erg-ml
```

If you already cloned without `--recursive`:
```bash
git submodule update --init --recursive
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with actual credentials
```

### 3. Install Dependencies

```bash
poetry install
```

## Running Locally

```bash
# Client name is auto-detected from config.py, but you can override:
# export CLIENT_NAME=erg

# List available tasks
poetry run python -m ml list-tasks

# Run training
poetry run python -m ml train --task advanced_power_forecast

# Run predictions
poetry run python -m ml predict --task advanced_power_forecast --start-date 2024-01-01
```

## Configuration

Edit `config.py` to:
- Set client name (auto-detected by CLI)
- Enable/disable tasks
- Configure database credentials
- Set Nomad schedules
- Adjust task parameters

## Deployment

### Build Docker Image

```bash
docker build -t ghcr.io/enlitia/service-erg-ml:latest .
```

### Deploy to Nomad

Nomad job files are managed in the `service-erg-data-infra` repository under `nomad/jobs/ml/`.

See the data-infra repository for deployment instructions.
