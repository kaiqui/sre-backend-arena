import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "version" in data
    assert "dependencies" in data

def test_liveness_probe():
    response = client.get("/api/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

def test_readiness_probe():
    response = client.get("/api/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
