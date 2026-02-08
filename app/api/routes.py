from fastapi import APIRouter, HTTPException, status

from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.llm_client import get_llm_client

router = APIRouter()


@router.post("/generate", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def generate_response(request: PromptRequest) -> PromptResponse:
    """
    Generate a response from the configured LLM provider.
    
    Works with any OpenAI-compatible API (Groq, OpenAI, Azure, etc.)
    based on environment variable configuration.
    """
    client = await get_llm_client()

    try:
        async with client:
            response = await client.generate(request.prompt)
            return PromptResponse(response=response)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

