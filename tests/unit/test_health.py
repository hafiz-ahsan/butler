"""Test health endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_main_health_endpoint(client: TestClient):
    """Test main health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Butler"
    assert "version" in data


def test_api_health_endpoint(client: TestClient):
    """Test API health endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Butler"
    assert "version" in data


def test_readiness_check(client: TestClient):
    """Test readiness check endpoint."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ready"


def test_liveness_check(client: TestClient):
    """Test liveness check endpoint."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "alive"
