"""
HireSense AI — AsyncOpenAI Client Wrapper

Provides:
  - stream_text()  → async generator of raw text chunks (for question streaming)
  - stream_json()  → async generator of raw text chunks (for structured JSON endpoints)
  - complete()     → awaitable single-shot response (not used in MVP but useful for testing)
"""

import logging
from typing import AsyncGenerator
from openai import AsyncOpenAI, APIError, RateLimitError, APIConnectionError
import asyncio

from app.config import get_settings

logger = logging.getLogger(__name__)


def _get_client() -> AsyncOpenAI:
    """Lazily create the AsyncOpenAI client using the cached settings."""
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.openai_api_key)


async def stream_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    max_retries: int = 3,
) -> AsyncGenerator[str, None]:
    """
    Stream raw text tokens from OpenAI.

    Yields individual text delta chunks as they arrive.
    Implements exponential back-off retry on transient errors.
    """
    settings = get_settings()
    client = _get_client()

    for attempt in range(1, max_retries + 1):
        try:
            stream = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            return  # Successful completion — exit retry loop

        except RateLimitError:
            if attempt == max_retries:
                raise
            wait = 2 ** attempt
            logger.warning(f"OpenAI rate limit hit. Retrying in {wait}s (attempt {attempt}/{max_retries})")
            await asyncio.sleep(wait)

        except APIConnectionError:
            if attempt == max_retries:
                raise
            wait = 2 ** attempt
            logger.warning(f"OpenAI connection error. Retrying in {wait}s (attempt {attempt}/{max_retries})")
            await asyncio.sleep(wait)

        except APIError as exc:
            logger.error(f"OpenAI API error: {exc}")
            raise


async def stream_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> AsyncGenerator[str, None]:
    """
    Stream a JSON-mode response from OpenAI.

    Uses response_format=json_object to guarantee parseable JSON output.
    Yields raw text chunks; the SSE layer is responsible for accumulation + parsing.
    """
    settings = get_settings()
    client = _get_client()

    stream = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        response_format={"type": "json_object"},
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


async def complete(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> str:
    """
    Non-streaming single-shot completion. Returns the full response text.
    Useful for testing and for cases where streaming is not needed.
    """
    settings = get_settings()
    client = _get_client()

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content or ""
