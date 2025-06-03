"""Tests for content moderation API routes."""

import pytest
from fastapi.testclient import TestClient

from classifier_demo.main import create_app
from classifier_demo.services.content_moderation_service import ContentModerationService


@pytest.fixture
def client():
    """Fixture to provide a test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def moderation_service():
    """Fixture to provide a ContentModerationService instance."""
    service = ContentModerationService.initialize()
    yield service
    service.cleanup()


def test_moderate_endpoint_success(client):
    """Test successful content moderation request."""
    # Test with safe content
    response = client.post(
        "/content-moderation/moderate",
        json={"text": "Hello, how are you today?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert isinstance(data["scores"], dict)
    assert "Safe Content" in data["scores"]
    assert data["scores"]["Safe Content"] > 0.5


def test_moderate_endpoint_harmful_content(client):
    """Test content moderation with potentially harmful content."""
    response = client.post(
        "/content-moderation/moderate",
        json={"text": "I hate you and want to hurt you"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert isinstance(data["scores"], dict)
    assert "Violence" in data["scores"]
    assert data["scores"]["Violence"] > 0.5


def test_moderate_endpoint_invalid_request(client):
    """Test content moderation with invalid request."""
    # Missing text field
    response = client.post(
        "/content-moderation/moderate",
        json={},
    )
    assert response.status_code == 422

    # Invalid type for text field
    response = client.post(
        "/content-moderation/moderate",
        json={"text": 123},
    )
    assert response.status_code == 422
