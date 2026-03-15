#!/bin/bash
set -e
echo "Validating SRE Backend Arena (NestJS) submission..."

required_files=(
    "src/main.ts"
    "src/app.module.ts"
    "src/battle/battle.controller.ts"
    "src/battle/battle.service.ts"
    "src/pokemon/pokemon.service.ts"
    "src/external-api/external-api.service.ts"
    "src/cache/cache.service.ts"
    "package.json"
    "Dockerfile"
    "k8s/deployment.yaml"
    "terraform/datadog/slo.tf"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
done

echo "All required files present!"
echo "Running tests..."
npm run test:cov
echo "Validation successful!"
