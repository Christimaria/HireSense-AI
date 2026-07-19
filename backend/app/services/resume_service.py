"""
HireSense AI — Resume Review Service

Stateless service layer sitting between the API router and the AI client.
Its sole responsibility is to build the prompt and delegate streaming to
the Gemini client — no I/O, no database, no side effects.

Privacy guarantee: resume_text is never stored, cached, or logged in full.
It exists in memory only for the duration of this async generator.
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.resume_prompts import RESUME_SYSTEM_PROMPT, build_resume_review_prompt

logger = logging.getLogger(__name__)


async def stream_resume_review(
    resume_text: str,
    target_role: str | None,
) -> AsyncGenerator[str, None]:
    """
    Yield raw JSON text chunks from Gemini for a resume review.

    The SSE helper (utils/sse.py → stream_json_object) wraps this generator:
      1. Each chunk is forwarded to the client as a `chunk` SSE event
         (enables a typing / progress animation in the UI).
      2. After the stream ends, the full accumulated text is JSON-parsed
         and emitted as a final `result` SSE event containing the structured
         ResumeReviewResponse object.
      3. A `[DONE]` sentinel closes the stream.

    Args:
        resume_text: Validated, stripped plain-text resume content.
        target_role: Optional job title provided by the user.

    Yields:
        Raw text delta strings from the Gemini streaming response.
    """
    logger.info(
        "Resume review started | target_role=%r | chars=%d",
        target_role or "unspecified",
        len(resume_text),
    )

    user_prompt = build_resume_review_prompt(resume_text, target_role)

    async for chunk in ai_client.stream_json(
        system_prompt=RESUME_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,   # Low temperature for consistent, deterministic scoring
        max_tokens=2000,
    ):
        yield chunk

    logger.info("Resume review stream complete | target_role=%r", target_role or "unspecified")
