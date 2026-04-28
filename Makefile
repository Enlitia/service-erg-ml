.DEFAULT_GOAL := help

RUN_COMMAND ?= poetry run

.SILENT:

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# CLEAN -------------------------------------------------------------------------------------------
pyc-clean: ## Remove python byte code files
	find . -iname "*.pyc" -delete

rm-venv-clean: ## Remove the virtual environment
	-poetry env remove python

clean: pyc-clean rm-venv-clean ## Cleans the environment

# DEV-SETUP ---------------------------------------------------------------------------------------
hooks:  ## Installs git hooks
	$(RUN_COMMAND) pre-commit install
	$(RUN_COMMAND) pre-commit install --hook-type commit-msg

deps: ## Installs all project package dependencies
	poetry install

dev-setup: deps hooks ##Sets up the development environment

# FORMAT ------------------------------------------------------------------------------------------
format:  ## Formats the code
	$(RUN_COMMAND) ruff format .

# STATIC ANALYSES ---------------------------------------------------------------------------------
type-analysis: ## Checks the code regarding types
	$(RUN_COMMAND) mypy .

lint-analysis:  ## Lints the code
	$(RUN_COMMAND) ruff check . --fix

static-analysis: lint-analysis type-analysis ## Checks the code for errors and inconsistency
