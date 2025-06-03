"""Routes for content moderation API.

This module provides FastAPI routes for content moderation functionality,
allowing text content to be analyzed and scored across different categories.
"""

from typing import Annotated, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from classifier_demo.services.content_moderation_service import (
    ContentModerationService,
)

# Initialize router with prefix and tags for API documentation
router = APIRouter(
    prefix="/content-moderation",
    tags=["content-moderation"],
)


def get_moderation_service() -> ContentModerationService:
    """Get an instance of the content moderation service.

    Returns:
        ContentModerationService: A configured instance of the moderation service.
    """
    return ContentModerationService()


class ModerationRequest(BaseModel):
    """Request model for content moderation.

    Attributes:
        text: The text content to be analyzed for moderation.
    """

    text: str


class ModerationResponse(BaseModel):
    """Response model for content moderation results.

    Attributes:
        scores: Dictionary mapping category names to their moderation scores.
    """

    scores: Dict[str, float]


@router.post("/moderate", response_model=ModerationResponse)
async def moderate_content(
    moderation_request: ModerationRequest,
    service: Annotated[ContentModerationService, Depends(get_moderation_service)],
) -> ModerationResponse:
    """Moderate the provided text content and return category scores.

    Args:
        moderation_request: The request containing the text to moderate.
        service: The content moderation service instance.

    Returns:
        ModerationResponse: The moderation scores for different categories.
    """
    scores = service.moderate_text(moderation_request.text)
    return ModerationResponse(scores=scores)
