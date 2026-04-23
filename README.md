# Service ERG ML

ERG client deployment for the Core ML Platform.

## Overview

This repository contains only configuration and deployment files for the ERG client. All ML logic resides in the `core-ml-platform` submodule.

## Repository Structure

```
service-erg-ml/
├── core-ml-platform/          # Git submodule - the complete ML framework
├── config.py                  # ERG-specific configuration
├── run.sh                     # CLI wrapper script
├── Makefile                   # Convenient commands
├── ops/
│   ├── nomad/                 # Nomad deployment files
│   │   ├── advanced_power_forecast-train.hcl
│   │   └── advanced_power_forecast-predict.hcl
│   └── update_nomad_configs.py
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
make install
# OR
cd core-ml-platform && poetry install
```

## Running Locally

### Using Make (Easiest)

```bash
# List available tasks
make list-tasks

# Run training
make train

# Run predictions
make predict
```

### Using run.sh Script

```bash
# Train a specific task
./run.sh train --task advanced_power_forecast

# Generate predictions
./run.sh predict --task advanced_power_forecast

# List all available tasks
./run.sh list-tasks
```

### Direct CLI Usage

```bash
cd core-ml-platform
poetry run python -m core_ml.cli ml train --task advanced_power_forecast
```

## Configuration

Edit `config.py` to:
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

```bash
# Deploy jobs
nomad job run ops/nomad/advanced_power_forecast-train.hcl
nomad job run ops/nomad/advanced_power_forecast-predict.hcl
```

