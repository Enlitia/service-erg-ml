# Service ERG ML

ERG client deployment for the Core ML Platform.

## Overview

This repository contains only configuration and deployment files for the ERG client. All ML logic resides in the `core-ml-platform` submodule.

## Repository Structure

```
service-erg-ml/
├── core-ml-platform/          # Git submodule - the complete ML framework
├── config.py                  # ERG-specific configuration
├── ops/
│   ├── nomad/                 # Nomad deployment files
│   │   ├── advanced_power_forecast-train.hcl
│   │   └── advanced_power_forecast-predict.hcl
│   └── update_nomad_configs.py
├── Dockerfile                 # Builds ERG container with framework
├── .env.example               # Environment variables template
└── README.md
```

## Setup

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

## Configuration

Edit `config.py` to configure ERG-specific settings.

## Deployment

Build and deploy using Docker and Nomad.

