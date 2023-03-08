PROJECT_NAME := "ipams"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: setup run ## run everything

test: pre-commit-all unit integration ## Run all tests

setup: ## install required modules
	python -m pip install -U -r requirements.txt
	python -m pip install -U -r requirements-dev.txt
	pre-commit install

unit: ## run unit tests
	python -m pytest -vvl tests/unit/ --showlocals

integration: ## run integration tests
	python -m pytest -vvl --setup-show -vvl tests/integration/ --showlocals

run: ## run project
	python -m $(PROJECT_NAME)

clean: ## clean cache and temp dirs
	rm -rf ./.mypy_cache ./.pytest_cache
	rm -f .coverage

pre-commit-all: ## run pre-commit on all files
	pre-commit run --all-files

pre-commit: ## run pre-commit
	pre-commit run
