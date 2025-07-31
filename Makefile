.PHONY: help install dev test lint format clean

# Default target
help:
	@echo "Butler - A Python backend service"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies using uv"
	@echo "  dev          - Start development server"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Clean cache and build files"

# Install dependencies
install:
	uv sync

# Install development dependencies
install-dev:
	uv sync --all-extras --dev
	pre-commit install

# Start development server
dev:
	./scripts/dev.sh

# Run tests
test:
	uv run pytest tests/ -v

# Run tests with coverage
test-cov:
	uv run pytest tests/ -v --cov=butler --cov-report=term-missing --cov-report=html

# Run linting
lint:
	uv run black --check --diff .
	uv run isort --check-only --diff .
	uv run flake8 .
	uv run mypy src/butler
	uv run bandit -r src/butler
	uv run safety check

# Format code
format:
	uv run black .
	uv run isort .

# Security check
security:
	uv run bandit -r src/butler
	uv run safety check

# Clean cache and build files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

# Database commands (when using Alembic)
db-migrate:
	uv run alembic upgrade head

db-migration:
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

db-downgrade:
	uv run alembic downgrade -1

# Health check
health:
	curl -f http://localhost:8000/health || exit 1