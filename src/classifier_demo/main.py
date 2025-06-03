"""FastAPI application for Heroes and Movies API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from classifier_demo.api import content_moderation_route
from classifier_demo.middleware.rps_tracker import RPSTrackerMiddleware
from classifier_demo.services.content_moderation_service import (
    ContentModerationService,
)

app = FastAPI(title="Heroes and Movies API")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for FastAPI."""
    # Initialize content moderation service and download model
    print("Initializing content moderation service and downloading model...")
    content_moderation = ContentModerationService.initialize()
    print("Content moderation service initialized successfully!")

    yield

    content_moderation.cleanup()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Classifier service API", version="1.0.0", lifespan=lifespan)

    # Add RPS tracker middleware
    app.add_middleware(RPSTrackerMiddleware)

    app.include_router(content_moderation_route.router)

    return app


app = create_app()
