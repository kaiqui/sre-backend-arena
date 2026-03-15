.PHONY: help install test lint build docker-build docker-run k8s-deploy clean

help:
	@echo "Available commands:"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run ktlint"
	@echo "  make build        - Build JAR"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make k8s-deploy   - Deploy to Kubernetes"
	@echo "  make clean        - Clean artifacts"

test:
	./gradlew test

lint:
	./gradlew ktlintCheck

build:
	./gradlew shadowJar

docker-build:
	docker build -t wizard-api:latest .

docker-run:
	docker-compose up -d

k8s-deploy:
	kubectl apply -f k8s/

clean:
	./gradlew clean
