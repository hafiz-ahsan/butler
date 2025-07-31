"""AI service endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from butler.api.endpoints.auth import User, get_current_user
from butler.core.logging import get_logger
from butler.services.ai_service import AIService

router = APIRouter()
logger = get_logger(__name__)


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str = Field(..., description="The user's message")
    provider: str = Field(
        default="openai", description="AI provider (openai, anthropic, google)"
    )
    model: Optional[str] = Field(None, description="Specific model to use")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation")


class ChatResponse(BaseModel):
    """Chat response model."""

    message: str
    provider: str
    model: str
    usage: dict


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """Chat with AI service."""
    logger.info(
        "AI chat request",
        user_id=current_user.id,
        provider=request.provider,
        model=request.model,
    )

    try:
        ai_service = AIService()
        response = await ai_service.chat(
            message=request.message,
            provider=request.provider,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        logger.info(
            "AI chat response generated",
            user_id=current_user.id,
            provider=request.provider,
            tokens_used=response.get("usage", {}).get("total_tokens", 0),
        )

        return ChatResponse(**response)

    except ValueError as e:
        logger.error("Invalid AI provider", provider=request.provider, error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            "AI service error",
            user_id=current_user.id,
            provider=request.provider,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail="AI service unavailable")


@router.get("/providers")
async def get_available_providers(current_user: User = Depends(get_current_user)):
    """Get available AI providers and their status."""
    ai_service = AIService()
    providers = await ai_service.get_available_providers()

    return {"providers": providers}
