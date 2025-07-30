"""Test authentication endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, sample_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_login_user(client: TestClient, sample_user_data):
    """Test user login."""
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_get_current_user_info(client: TestClient, sample_user_data):
    """Test getting current user info."""
    # First register and get token
    register_response = client.post("/api/v1/auth/register", json=sample_user_data)
    token = register_response.json()["access_token"]
    
    # Get user info with token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert "is_active" in data


def test_get_current_user_info_unauthorized(client: TestClient):
    """Test getting current user info without token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403  # No authorization header


def test_get_current_user_info_invalid_token(client: TestClient):
    """Test getting current user info with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401


def test_refresh_token(client: TestClient, sample_user_data):
    """Test token refresh."""
    # First register and get token
    register_response = client.post("/api/v1/auth/register", json=sample_user_data)
    token = register_response.json()["access_token"]
    
    # Refresh token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/auth/refresh", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data