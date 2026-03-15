.PHONY: help install test lint build docker-build docker-run k8s-deploy clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make build        - Build application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run with Docker Compose"
	@echo "  make k8s-deploy   - Deploy to Kubernetes"
	@echo "  make clean        - Clean artifacts"

install:
	npm ci

test:
	npm run test:cov

lint:
	npm run lint

build:
	npm run build

docker-build:
	docker build -t pokemon-battle-api:latest .

docker-run:
	docker-compose up -d

k8s-deploy:
	kubectl apply -f k8s/

clean:
	rm -rf dist coverage node_modules
