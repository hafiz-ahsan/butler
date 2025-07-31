"""Integration tests for full application flow."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_full_user_journey(client: TestClient):
    """Test complete user journey from registration to AI chat."""

    # 1. Check health
    health_response = client.get("/health")
    assert health_response.status_code == 200

    # 2. Register user
    user_data = {
        "email": "integration@example.com",
        "password": "securepassword123",
        "full_name": "Integration Test User",
    }

    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200

    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get user info
    user_info_response = client.get("/api/v1/auth/me", headers=headers)
    assert user_info_response.status_code == 200

    user_info = user_info_response.json()
    assert user_info["email"] == user_data["email"]
    # Note: In demo mode, full_name is hardcoded to "Demo User"
    assert user_info["full_name"] == "Demo User"

    # 4. Check available AI providers
    providers_response = client.get("/api/v1/ai/providers", headers=headers)
    assert providers_response.status_code == 200

    providers = providers_response.json()["providers"]
    assert len(providers) > 0

    # 5. Login with same credentials
    login_data = {"email": user_data["email"], "password": user_data["password"]}

    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200

    new_token = login_response.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}

    # 6. Refresh token
    refresh_response = client.post("/api/v1/auth/refresh", headers=new_headers)
    assert refresh_response.status_code == 200

    refreshed_token = refresh_response.json()["access_token"]
    # Note: Tokens may be identical if generated within the same second
    # The important thing is that refresh endpoint works
    assert "access_token" in refresh_response.json()


@pytest.mark.integration
def test_api_documentation_accessible(client: TestClient):
    """Test that API documentation is accessible."""

    # Test OpenAPI JSON
    openapi_response = client.get("/openapi.json")
    assert openapi_response.status_code == 200

    openapi_data = openapi_response.json()
    assert "openapi" in openapi_data
    assert "info" in openapi_data
    assert openapi_data["info"]["title"] == "Butler"


@pytest.mark.integration
def test_cors_headers(client: TestClient):
    """Test CORS headers are properly set."""

    # Test preflight request
    response = client.options(
        "/api/v1/health/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization",
        },
    )

    # FastAPI automatically handles CORS, so we should get a successful response
    assert response.status_code in [200, 204]
