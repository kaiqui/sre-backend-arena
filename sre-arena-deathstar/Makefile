.PHONY: help install test lint format run docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make run          - Run application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make clean        - Clean artifacts"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src tests
	black --check src tests
	mypy src

format:
	black src tests
	isort src tests

run:
	python -m uvicorn src.main:app --reload

docker-build:
	docker build -t sre-backend-arena:latest .

docker-run:
	docker-compose up -d

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	rm -rf .coverage htmlcov
