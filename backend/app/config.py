"""
HireSense AI — Application Configuration

Reads all settings from environment variables / .env file.
The singleton is cached via @lru_cache so the file is parsed exactly once.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Google AI / Gemini ────────────────────────────────────────────────────
    gemini_api_key: str = Field(..., description="Google AI Studio API key")
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model name (e.g. gemini-2.5-flash, gemini-2.0-flash, gemini-flash-latest)",
    )

    @field_validator("gemini_model", mode="before")
    @classmethod
    def sanitize_gemini_model(cls, v: str | None) -> str:
        if not v or not isinstance(v, str):
            return "gemini-1.5-flash"
        val = v.strip()
        if val.startswith("models/"):
            val = val[7:]
        return val

    # ── Server ────────────────────────────────────────────────────────────────
    environment: str = Field(default="development")
    port: int = Field(default=8000)

    # ── CORS ──────────────────────────────────────────────────────────────────
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins",
    )

    # ── Computed properties ───────────────────────────────────────────────────
    @property
    def allowed_origins_list(self) -> list[str]:
        if self.allowed_origins.strip() == "*":
            return ["*"]
        origins = []
        for o in self.allowed_origins.split(","):
            cleaned = o.strip().rstrip("/")
            if cleaned:
                origins.append(cleaned)
        return origins or ["*"]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — import and call get_settings() anywhere."""
    return Settings()
