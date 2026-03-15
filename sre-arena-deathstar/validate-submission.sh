#!/bin/bash
set -e
echo "Validating SRE Backend Arena (FastAPI) submission..."

required_files=(
    "src/main.py"
    "src/config/settings.py"
    "src/api/routes/health.py"
    "src/api/routes/deathstar.py"
    "src/services/ship_service.py"
    "src/resilience/circuit_breaker.py"
    "Dockerfile"
    "requirements.txt"
    "k8s/deployment.yaml"
    "terraform/k8s/deployment.tf"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
done

echo "All required files present!"
echo "Validation successful!"
