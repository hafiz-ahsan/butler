"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from butler.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str
    version: str


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check for container orchestration."""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Liveness check for container orchestration."""
    return {"status": "alive"}