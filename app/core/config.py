from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This configuration is provider-agnostic and works with any OpenAI-compatible API.
    Supports multiple LLM providers: Groq, OpenAI, Azure OpenAI, etc.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Provider Configuration
    llm_api_key: str
    llm_base_url: str
    llm_model: str

    # Optional Settings
    api_timeout: int = 60

    # Optional: Provider name for logging/monitoring (not used in API calls)
    llm_provider: str = "generic"


settings = Settings()
