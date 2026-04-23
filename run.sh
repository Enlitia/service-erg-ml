#!/bin/bash
# Run ML tasks for ERG client using core-ml-platform

set -e

# Change to core-ml-platform directory
cd "$(dirname "$0")/core-ml-platform"

# Ensure dependencies are installed
if [ ! -d ".venv" ]; then
    echo "Installing core-ml-platform dependencies..."
    poetry install
fi

# Set environment variables for ERG
export CLIENT_NAME=erg
export CLIENT_CONFIG_PATH="$(dirname "$0")/config.py"
export PYTHONPATH="$(pwd)/src:$(dirname "$0"):$PYTHONPATH"

# Load .env if it exists
if [ -f "$(dirname "$0")/.env" ]; then
    export $(cat "$(dirname "$0")/.env" | grep -v '^#' | xargs)
fi

# Run the CLI with all arguments passed through
poetry run python -m core_ml.cli ml "$@"
