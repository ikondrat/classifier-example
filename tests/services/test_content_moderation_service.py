import time

import pytest

from classifier_demo.services.content_moderation_service import (
    ContentModerationService,
)


@pytest.fixture
def moderation_service():
    """Fixture to provide a ContentModerationService instance."""
    service = ContentModerationService.initialize()
    yield service
    service.cleanup()


def test_singleton_pattern():
    """Test that ContentModerationService follows singleton pattern."""
    service1 = ContentModerationService.initialize()
    service2 = ContentModerationService.initialize()
    assert service1 is service2
    service1.cleanup()


def test_moderate_text(moderation_service):
    """Test text moderation functionality."""
    # Test with safe content
    safe_text = "Hello, how are you today?"
    result = moderation_service.moderate_text(safe_text)
    assert isinstance(result, dict)
    assert "Safe Content" in result
    assert result["Safe Content"] > 0.5  # Should be classified as safe

    # Test with potentially harmful content
    harmful_text = "I hate you and want to hurt you"
    result = moderation_service.moderate_text(harmful_text)
    assert isinstance(result, dict)
    assert "Violence" in result
    assert result["Violence"] > 0.5  # Should detect violence


def test_request_rate_tracking(moderation_service):
    """Test request rate tracking functionality."""
    # Make some requests
    for _ in range(5):
        moderation_service.moderate_text("Test message")
        time.sleep(0.1)  # Small delay between requests

    rate = moderation_service.get_request_rate()
    assert isinstance(rate, float)
    assert rate > 0


def test_cleanup():
    """Test cleanup functionality."""
    # Create a new instance
    service = ContentModerationService.initialize()
    assert service._initialized is True

    # Cleanup
    service.cleanup()
    assert service._initialized is False
    assert service._instance is None


def test_category_mapping(moderation_service):
    """Test that all categories are properly mapped."""
    text = "Test message"
    result = moderation_service.moderate_text(text)

    # Check that all categories in the mapping are present in the result
    for category in moderation_service.CATEGORY_MAPPING.values():
        assert category in result
        assert isinstance(result[category], float)
        assert 0 <= result[category] <= 1
