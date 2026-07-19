"""
HireSense AI — Google Gemini AI Client

Wraps the official google-genai SDK with an async-first interface used
by all service layers. The public API is intentionally identical to the
former OpenAI client so every service file stays unchanged.

Public functions
────────────────
  stream_text(system, user, temperature, max_tokens) → AsyncGenerator[str]
      Streams raw text tokens. Used for interview question generation.

  stream_json(system, user, temperature, max_tokens) → AsyncGenerator[str]
      Streams JSON text tokens. The SSE helper accumulates them and emits
      a final parsed `result` event. Used for Resume Review, Evaluation, etc.

  complete(system, user, temperature, max_tokens) → str
      Single-shot non-streaming call. Returns the full response string.
      Useful for testing and low-latency, short-output endpoints.
"""

import asyncio
import logging
from functools import lru_cache
from typing import AsyncGenerator

from google import genai
from google.genai import types

from app.config import get_settings

logger = logging.getLogger(__name__)

# ── Retry configuration ───────────────────────────────────────────────────────
_MAX_RETRIES = 3
_RETRYABLE_CODES = ("429", "500", "503", "resource_exhausted", "internal", "unavailable")


def _is_retryable(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(code in msg for code in _RETRYABLE_CODES)


# ── Client factory ────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _get_client() -> genai.Client:
    """
    Lazily create and cache the Gemini client for the process lifetime.
    The lru_cache ensures we never open more than one client instance.
    """
    settings = get_settings()
    return genai.Client(api_key=settings.gemini_api_key)


def _text_config(system_prompt: str, temperature: float, max_tokens: int) -> types.GenerateContentConfig:
    """Build a plain-text GenerateContentConfig."""
    return types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )


def _json_config(system_prompt: str, temperature: float, max_tokens: int) -> types.GenerateContentConfig:
    """
    Build a JSON-mode GenerateContentConfig.
    response_mime_type="application/json" instructs Gemini to return only
    valid JSON — equivalent to OpenAI's response_format={"type":"json_object"}.
    """
    enforced_system = (
        system_prompt.rstrip()
        + "\n\nIMPORTANT: Return ONLY a raw JSON object. "
          "No markdown fences, no backticks, no prose outside the JSON."
    )
    return types.GenerateContentConfig(
        system_instruction=enforced_system,
        temperature=temperature,
        max_output_tokens=max_tokens,
        response_mime_type="application/json",
    )


# ── Public streaming functions ────────────────────────────────────────────────
async def stream_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> AsyncGenerator[str, None]:
    """
    Stream plain-text tokens from Gemini with exponential-back-off retry
    on transient errors (rate-limits, 5xx responses).
    """
    client = _get_client()
    settings = get_settings()
    config = _text_config(system_prompt, temperature, max_tokens)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            async for chunk in await client.aio.models.generate_content_stream(
                model=settings.gemini_model,
                contents=user_prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
            return  # success — exit retry loop

        except Exception as exc:
            if attempt == _MAX_RETRIES or not _is_retryable(exc):
                logger.error("stream_text failed (attempt %d): %s", attempt, exc)
                raise
            wait = 2 ** attempt
            logger.warning(
                "stream_text transient error (attempt %d/%d), retrying in %ds — %s",
                attempt, _MAX_RETRIES, wait, exc,
            )
            await asyncio.sleep(wait)


async def stream_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> AsyncGenerator[str, None]:
    """
    Stream JSON tokens from Gemini.
    response_mime_type forces clean JSON output. The SSE helper in
    utils/sse.py accumulates the chunks and parses the final object.
    """
    client = _get_client()
    settings = get_settings()
    config = _json_config(system_prompt, temperature, max_tokens)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            async for chunk in await client.aio.models.generate_content_stream(
                model=settings.gemini_model,
                contents=user_prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
            return

        except Exception as exc:
            if attempt == _MAX_RETRIES or not _is_retryable(exc):
                logger.error("stream_json failed (attempt %d): %s", attempt, exc)
                raise
            wait = 2 ** attempt
            logger.warning(
                "stream_json transient error (attempt %d/%d), retrying in %ds — %s",
                attempt, _MAX_RETRIES, wait, exc,
            )
            await asyncio.sleep(wait)


async def complete(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> str:
    """
    Non-streaming single-shot JSON completion.
    Returns the full response as a string.
    """
    client = _get_client()
    settings = get_settings()
    config = _json_config(system_prompt, temperature, max_tokens)

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=user_prompt,
        config=config,
    )
    return response.text or ""
