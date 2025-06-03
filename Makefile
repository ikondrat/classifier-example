.PHONY: install
install:
	@echo "Installing with optional dependencies..."
	uv sync --all-groups

.PHONY: test
test:
	@echo "Running tests..."
	PYTHONPATH=$(PWD) uv run pytest

.PHONY: lint
lint:
	@echo "Linting project with ruff..."
	uv run ruff check

.PHONY: type-check
type-check:
	@echo "Checking types with mypy..."
	uv run mypy --explicit-package-bases src/classifier_demo

.PHONY: format-check
format-check:
	@echo "Checking format with ruff..."
	uv run ruff format --check

.PHONY: validate
validate: lint type-check format-check

.PHONY: format
format:
	@echo "Formatting project with ruff..."
	uv run ruff format
	uv run ruff check --fix

.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: run
run: install
	@echo "Starting FastAPI application..."
	PYTHONPATH=$(PWD)/src uv run uvicorn classifier_demo.main:app --reload

