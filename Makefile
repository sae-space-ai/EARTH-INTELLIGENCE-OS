.PHONY: install format lint typecheck test test-unit test-integration compose-up compose-down migrate api worker check clean

# Installation
install:
	pip install -e ".[dev]"
	pre-commit install

# Code quality
format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy packages apps services

# Testing
test:
	pytest

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

# Docker
compose-up:
	docker compose up -d

compose-down:
	docker compose down

# Database
migrate:
	alembic upgrade head

# Services
api:
	uvicorn apps.api.main:app --host $(or $(API_HOST),0.0.0.0) --port $(or $(API_PORT),8000) --reload

worker:
	python -m apps.worker.main

# Validation
check: lint typecheck test

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	rm -rf dist build .eggs *.egg-info
