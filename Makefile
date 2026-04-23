.PHONY: help install train predict list-tasks clean

help:
	@echo "ERG ML Service - Available commands:"
	@echo ""
	@echo "  make install      - Install core-ml-platform dependencies"
	@echo "  make train        - Run training for all tasks"
	@echo "  make predict      - Run predictions for all tasks"
	@echo "  make list-tasks   - List available ML tasks"
	@echo "  make clean        - Clean up build artifacts"
	@echo ""
	@echo "Direct CLI usage:"
	@echo "  ./run.sh train --task advanced_power_forecast"
	@echo "  ./run.sh predict --task advanced_power_forecast"

install:
	cd core-ml-platform && poetry install

train:
	./run.sh train --task advanced_power_forecast

predict:
	./run.sh predict --task advanced_power_forecast

list-tasks:
	./run.sh list-tasks

clean:
	cd core-ml-platform && rm -rf .venv __pycache__ .pytest_cache .mypy_cache .ruff_cache
