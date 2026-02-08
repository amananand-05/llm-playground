from typing import Any

import httpx

from app.core.config import settings


class LLMClient:
    """
    Generic LLM client that works with any OpenAI-compatible API.
    
    Supports multiple providers:
    - Groq (https://api.groq.com/openai)
    - OpenAI (https://api.openai.com)
    - Azure OpenAI
    - Any OpenAI-compatible API
    
    Configuration is done via environment variables.
    """

    def __init__(self) -> None:
        self.base_url = settings.llm_base_url
        self.api_key = settings.llm_api_key
        self.model_name = settings.llm_model
        self.timeout = settings.api_timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "LLMClient":
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(self.timeout),
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM based on the prompt.
        
        Args:
            prompt: User input text
            
        Returns:
            Generated response text
            
        Raises:
            RuntimeError: If API request fails or response is invalid
        """
        if not self._client:
            raise RuntimeError("LLMClient must be used as an async context manager")

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            response = await self._client.post("/v1/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"LLM API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Request failed: {str(e)}") from e
        except (KeyError, IndexError) as e:
            raise RuntimeError("Invalid response format from LLM API") from e


async def get_llm_client() -> LLMClient:
    """Factory function to create an LLM client instance."""
    return LLMClient()
