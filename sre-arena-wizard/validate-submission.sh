#!/bin/bash
set -e
echo "Validating SRE Backend Arena (Kotlin) submission..."

required_files=(
    "src/main/kotlin/com/srearena/Application.kt"
    "src/main/kotlin/com/srearena/WizardService.kt"
    "src/main/kotlin/com/srearena/CacheService.kt"
    "src/main/kotlin/com/srearena/ExternalApiClient.kt"
    "build.gradle.kts"
    "Dockerfile"
    "k8s/deployment.yaml"
    "terraform/k8s/deployment.tf"
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
./gradlew test
echo "Validation successful!"
