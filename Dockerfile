FROM python:3.12

ARG SM_SETTINGS_MODULE
ARG DB_USER
ARG DB_PASSWORD

WORKDIR /app

RUN apt-get update && apt-get install -y \
    openssh-client \
    gcc \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip and configure it in one step
RUN pip install --no-cache-dir poetry==1.8.3 && \
    python -m poetry config virtualenvs.create false

# Copy core-ml-platform and install it
COPY core-ml-platform /app/core-ml-platform
WORKDIR /app/core-ml-platform
RUN python -m poetry install --no-interaction --no-cache --no-ansi

# Copy ERG configuration
WORKDIR /app
COPY config.py /app/config.py

# Set environment variables
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV SM_SETTINGS_MODULE=${SM_SETTINGS_MODULE}
ENV CLIENT_NAME=erg
ENV CLIENT_CONFIG_PATH=/app/config.py
ENV PYTHONPATH=/app/core-ml-platform/src:/app

# CLI entry point from core-ml-platform
CMD ["python", "-m", "core_ml.cli"]

