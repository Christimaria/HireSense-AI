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


_FALLBACK_MODEL = "gemini-1.5-flash"


def _is_model_unavailable_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return "not_found" in msg or "404" in msg or "no longer available" in msg


def _log_available_models_on_error(target_model: str, exc: Exception) -> None:
    """Helper to query and log all available models when a Gemini API call fails."""
    try:
        client = _get_client()
        models = [
            (m.name[7:] if getattr(m, "name", "").startswith("models/") else getattr(m, "name", str(m)))
            for m in client.models.list()
        ]
        logger.error(
            "Gemini request failed for model %r: %s | COMPLETE LIST OF AVAILABLE MODELS FOR YOUR API KEY: %s",
            target_model,
            exc,
            models,
        )
    except Exception as list_exc:
        logger.error(
            "Gemini request failed for model %r: %s | (Failed to fetch available models list: %s)",
            target_model,
            exc,
            list_exc,
        )


# ── Public streaming functions ────────────────────────────────────────────────
async def stream_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """
    Stream plain-text tokens from Gemini with exponential-back-off retry
    on transient errors (rate-limits, 5xx responses).
    """
    client = _get_client()
    settings = get_settings()
    target_model = model or settings.gemini_model
    config = _text_config(system_prompt, temperature, max_tokens)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            async for chunk in await client.aio.models.generate_content_stream(
                model=target_model,
                contents=user_prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
            return  # success — exit retry loop

        except Exception as exc:
            if _is_model_unavailable_error(exc) and target_model != _FALLBACK_MODEL:
                logger.warning(
                    "Model %r returned unavailable error (%s). Falling back to %r",
                    target_model, exc, _FALLBACK_MODEL,
                )
                try:
                    async for chunk in await client.aio.models.generate_content_stream(
                        model=_FALLBACK_MODEL,
                        contents=user_prompt,
                        config=config,
                    ):
                        if chunk.text:
                            yield chunk.text
                    return
                except Exception as fallback_exc:
                    _log_available_models_on_error(_FALLBACK_MODEL, fallback_exc)
                    raise fallback_exc

            if attempt == _MAX_RETRIES or not _is_retryable(exc):
                _log_available_models_on_error(target_model, exc)
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
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """
    Stream JSON tokens from Gemini.
    response_mime_type forces clean JSON output. The SSE helper in
    utils/sse.py accumulates the chunks and parses the final object.
    """
    client = _get_client()
    settings = get_settings()
    target_model = model or settings.gemini_model
    config = _json_config(system_prompt, temperature, max_tokens)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            async for chunk in await client.aio.models.generate_content_stream(
                model=target_model,
                contents=user_prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
            return

        except Exception as exc:
            if _is_model_unavailable_error(exc) and target_model != _FALLBACK_MODEL:
                logger.warning(
                    "Model %r returned unavailable error (%s). Falling back to %r",
                    target_model, exc, _FALLBACK_MODEL,
                )
                try:
                    async for chunk in await client.aio.models.generate_content_stream(
                        model=_FALLBACK_MODEL,
                        contents=user_prompt,
                        config=config,
                    ):
                        if chunk.text:
                            yield chunk.text
                    return
                except Exception as fallback_exc:
                    _log_available_models_on_error(_FALLBACK_MODEL, fallback_exc)
                    raise fallback_exc

            if attempt == _MAX_RETRIES or not _is_retryable(exc):
                _log_available_models_on_error(target_model, exc)
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
    model: str | None = None,
) -> str:
    """
    Non-streaming single-shot JSON completion.
    Returns the full response as a string.
    """
    client = _get_client()
    settings = get_settings()
    target_model = model or settings.gemini_model
    config = _json_config(system_prompt, temperature, max_tokens)

    try:
        response = await client.aio.models.generate_content(
            model=target_model,
            contents=user_prompt,
            config=config,
        )
        return response.text or ""
    except Exception as exc:
        if _is_model_unavailable_error(exc) and target_model != _FALLBACK_MODEL:
            logger.warning("Model %r failed (%s). Falling back to %r", target_model, exc, _FALLBACK_MODEL)
            response = await client.aio.models.generate_content(
                model=_FALLBACK_MODEL,
                contents=user_prompt,
                config=config,
            )
            return response.text or ""
        _log_available_models_on_error(target_model, exc)
        raise
