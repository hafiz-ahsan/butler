"""AI service integration for multiple providers."""

from typing import Dict, List, Optional, Any
import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai

from butler.core.config import settings
from butler.core.logging import get_logger

logger = get_logger(__name__)


class AIService:
    """Service for interacting with multiple AI providers."""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.google_client = None
        
        # Initialize clients based on available API keys
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        
        if settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        
        if settings.google_ai_api_key:
            genai.configure(api_key=settings.google_ai_api_key)
            self.google_client = genai
    
    async def chat(
        self,
        message: str,
        provider: str = "openai",
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Send a chat message to the specified AI provider."""
        
        if provider == "openai":
            return await self._chat_openai(message, model, max_tokens, temperature)
        elif provider == "anthropic":
            return await self._chat_anthropic(message, model, max_tokens, temperature)
        elif provider == "google":
            return await self._chat_google(message, model, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    async def _chat_openai(
        self,
        message: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat with OpenAI API."""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        model = model or "gpt-3.5-turbo"
        max_tokens = max_tokens or 1000
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "message": response.choices[0].message.content,
                "provider": "openai",
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error("OpenAI API error", error=str(e))
            raise
    
    async def _chat_anthropic(
        self,
        message: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat with Anthropic API."""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
        
        model = model or "claude-3-sonnet-20240229"
        max_tokens = max_tokens or 1000
        
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": message}]
            )
            
            return {
                "message": response.content[0].text,
                "provider": "anthropic",
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            logger.error("Anthropic API error", error=str(e))
            raise
    
    async def _chat_google(
        self,
        message: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat with Google Generative AI."""
        if not self.google_client:
            raise ValueError("Google AI API key not configured")
        
        model_name = model or "gemini-pro"
        
        try:
            model_instance = genai.GenerativeModel(model_name)
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens or 1000,
                temperature=temperature
            )
            
            response = await model_instance.generate_content_async(
                message,
                generation_config=generation_config
            )
            
            return {
                "message": response.text,
                "provider": "google",
                "model": model_name,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                }
            }
        except Exception as e:
            logger.error("Google AI API error", error=str(e))
            raise
    
    async def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available AI providers and their status."""
        providers = []
        
        if self.openai_client:
            providers.append({
                "name": "openai",
                "status": "available",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
            })
        else:
            providers.append({
                "name": "openai",
                "status": "unavailable",
                "reason": "API key not configured"
            })
        
        if self.anthropic_client:
            providers.append({
                "name": "anthropic",
                "status": "available",
                "models": ["claude-3-sonnet-20240229", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
            })
        else:
            providers.append({
                "name": "anthropic",
                "status": "unavailable",
                "reason": "API key not configured"
            })
        
        if self.google_client:
            providers.append({
                "name": "google",
                "status": "available",
                "models": ["gemini-pro", "gemini-pro-vision"]
            })
        else:
            providers.append({
                "name": "google",
                "status": "unavailable",
                "reason": "API key not configured"
            })
        
        return providers