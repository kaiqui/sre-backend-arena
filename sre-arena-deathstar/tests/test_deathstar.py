import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_analyze_invalid_ship():
    response = client.post("/api/deathstar/analyze/99999")
    assert response.status_code == 404

def test_threat_statistics():
    response = client.get("/api/deathstar/threat-statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_ships_analyzed" in data
    assert "average_risk_score" in data
