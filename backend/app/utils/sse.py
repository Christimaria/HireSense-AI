"""
HireSense AI — SSE (Server-Sent Events) Utility Helpers
"""

import json
import logging
from typing import Any, AsyncGenerator

logger = logging.getLogger(__name__)


def sse_event(data: Any, event_type: str = "chunk") -> str:
    """
    Format a single SSE event string.

    Args:
        data: The payload — will be JSON-serialised if not a string.
        event_type: The SSE event type field (default 'chunk').

    Returns:
        A properly formatted SSE string ready to be streamed.
    """
    payload = json.dumps({"type": event_type, "content": data})
    return f"data: {payload}\n\n"


def sse_done() -> str:
    """Return the terminal [DONE] SSE event."""
    return "data: [DONE]\n\n"


def sse_error(message: str) -> str:
    """Return an error SSE event."""
    payload = json.dumps({"type": "error", "content": message})
    return f"data: {payload}\n\n"


async def stream_text_chunks(
    generator: AsyncGenerator[str, None],
) -> AsyncGenerator[str, None]:
    """
    Wraps an async text generator and yields properly formatted SSE events.
    Sends [DONE] at the end.
    """
    try:
        async for chunk in generator:
            if chunk:
                yield sse_event(chunk)
        yield sse_done()
    except Exception as exc:
        yield sse_error(str(exc))
        yield sse_done()





def _clean_json_text(text: str) -> str:
    """Safely strip markdown code block fences without stripping trailing text characters."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]
        else:
            cleaned = cleaned.lstrip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


async def stream_json_object(
    generator: AsyncGenerator[str, None],
) -> AsyncGenerator[str, None]:
    """
    Collects the full streamed text, then emits the complete JSON object
    in a single SSE event followed by [DONE].

    Used for endpoints that return structured JSON after streaming completes.
    """
    collected = []
    try:
        async for chunk in generator:
            if chunk:
                collected.append(chunk)
                # Stream incremental text so the UI shows typing animation
                yield sse_event(chunk, event_type="chunk")

        full_text = "".join(collected)

        # Try to parse and emit the final JSON object
        try:
            parsed = json.loads(full_text)
            yield sse_event(parsed, event_type="result")
        except json.JSONDecodeError:
            try:
                cleaned = _clean_json_text(full_text)
                parsed = json.loads(cleaned)
                yield sse_event(parsed, event_type="result")
            except Exception as parse_exc:
                logger.error("Failed to parse JSON response from Gemini: %s | raw_text: %r", parse_exc, full_text)
                yield sse_error(f"Failed to parse response format: {parse_exc}")

        yield sse_done()

    except Exception as exc:
        logger.error("SSE stream_json_object error: %s", exc, exc_info=True)
        yield sse_error(str(exc))
        yield sse_done()
