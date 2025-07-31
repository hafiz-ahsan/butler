"""API routes for Butler service."""

from fastapi import APIRouter

from butler.api.endpoints import ai, auth, health

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai-services"])
