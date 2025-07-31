"""Test AI service endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient) -> str:
    """Helper function to get auth token."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    return response.json()["access_token"]


def test_get_available_providers(client: TestClient):
    """Test getting available AI providers."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/ai/providers", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "providers" in data
    assert isinstance(data["providers"], list)


def test_chat_unauthorized(client: TestClient):
    """Test chat endpoint without authentication."""
    chat_data = {"message": "Hello, world!", "provider": "openai"}

    response = client.post("/api/v1/ai/chat", json=chat_data)
    assert response.status_code == 403


@patch('butler.services.ai_service.AIService.chat')
def test_chat_with_openai(mock_chat, client: TestClient):
    """Test chat with OpenAI provider."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Mock the AI service response
    mock_chat.return_value = {
        "message": "Hello! How can I help you today?",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }

    chat_data = {
        "message": "Hello, world!",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
    }

    response = client.post("/api/v1/ai/chat", json=chat_data, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Hello! How can I help you today?"
    assert data["provider"] == "openai"
    assert data["model"] == "gpt-3.5-turbo"
    assert "usage" in data


@patch('butler.services.ai_service.AIService.chat')
def test_chat_with_anthropic(mock_chat, client: TestClient):
    """Test chat with Anthropic provider."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Mock the AI service response
    mock_chat.return_value = {
        "message": "Hello! I'm Claude, how can I assist you?",
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }

    chat_data = {
        "message": "Hello, world!",
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
    }

    response = client.post("/api/v1/ai/chat", json=chat_data, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Hello! I'm Claude, how can I assist you?"
    assert data["provider"] == "anthropic"
    assert data["model"] == "claude-3-sonnet-20240229"


def test_chat_invalid_provider(client: TestClient):
    """Test chat with invalid provider."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    chat_data = {"message": "Hello, world!", "provider": "invalid_provider"}

    response = client.post("/api/v1/ai/chat", json=chat_data, headers=headers)
    assert response.status_code == 400


def test_chat_missing_message(client: TestClient):
    """Test chat without message."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    chat_data = {"provider": "openai"}

    response = client.post("/api/v1/ai/chat", json=chat_data, headers=headers)
    assert response.status_code == 422  # Validation error
