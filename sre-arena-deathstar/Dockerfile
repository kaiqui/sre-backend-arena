# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Install Datadog APM
RUN pip install --no-cache-dir ddtrace

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy application
COPY --from=build /app/src ./src
COPY --from=build /app/requirements.txt .
RUN chown -R appuser:appgroup /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DD_SERVICE=deathstar-analysis-api
ENV DD_ENV=production
ENV DD_VERSION=1.0.0
ENV DD_TRACE_ENABLED=true

# Start application
CMD ["ddtrace-run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]