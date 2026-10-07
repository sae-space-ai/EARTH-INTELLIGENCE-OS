.PHONY: install format lint typecheck test test-unit test-integration compose-up compose-down migrate api worker check clean up down logs demo smoke-test rc1-test

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

# RC1 Commands
up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

demo:
	@echo "Enabling demo mode..."
	@curl -s -X POST http://localhost:8000/api/v1/live/demo/enable
	@echo ""
	@echo "Demo mode enabled. Open http://localhost:3000"

smoke-test:
	@chmod +x scripts/rc1-smoke-test.sh
	@./scripts/rc1-smoke-test.sh

rc1-test:
	@echo "Running RC1 validation..."
	@echo ""
	@echo "1. Building containers..."
	@docker compose build
	@echo ""
	@echo "2. Starting services..."
	@docker compose up -d
	@echo ""
	@echo "3. Waiting for services to be healthy..."
	@sleep 10
	@echo ""
	@echo "4. Running smoke tests..."
	@chmod +x scripts/rc1-smoke-test.sh
	@./scripts/rc1-smoke-test.sh
