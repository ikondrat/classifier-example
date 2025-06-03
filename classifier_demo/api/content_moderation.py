"""Routes for content moderation API."""

from typing import Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from classifier_demo.services.content_moderation import ContentModerationService

router = APIRouter(prefix="/content-moderation", tags=["content-moderation"])


def get_moderation_service():
    """Dependency to get the service instance."""
    return ContentModerationService()


class ModerationRequest(BaseModel):
    """Request model."""

    text: str


class ModerationResponse(BaseModel):
    """Response model."""

    scores: Dict[str, float]


@router.post("/moderate", response_model=ModerationResponse)
async def moderate_content(
    moderation_request: ModerationRequest,
    service: ContentModerationService = Depends(get_moderation_service),  # noqa: B008
):
    """Moderate the provided text content and return category scores."""
    scores = service.moderate_text(moderation_request.text)

    return ModerationResponse(scores=scores)
