"""
HireSense AI — Application Configuration
Reads from environment variables / .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # ── OpenAI ──────────────────────────────────────────────────────────────
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model name")

    # ── Server ───────────────────────────────────────────────────────────────
    environment: str = Field(default="development")
    port: int = Field(default=8000)

    # ── CORS ─────────────────────────────────────────────────────────────────
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins",
    )

    # ── Rate Limiting ─────────────────────────────────────────────────────────
    rate_limit: str = Field(default="15/minute")

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — call get_settings() anywhere in the app."""
    return Settings()
