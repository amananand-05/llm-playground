from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Text prompt for the model")


class PromptResponse(BaseModel):
    response: str = Field(..., description="Generated response from the model")
