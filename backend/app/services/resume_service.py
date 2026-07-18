"""
HireSense AI — Resume Service
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
    Stream a structured resume review from the AI.

    The AI returns a JSON object; we stream it chunk-by-chunk so the
    frontend can show a typing animation. The SSE layer handles parsing
    the final assembled JSON.

    Privacy guarantee: resume_text is never persisted — it exists only
    for the duration of this async generator.
    """
    logger.info(
        "Starting resume review stream | target_role=%s | text_length=%d",
        target_role or "not specified",
        len(resume_text),
    )

    user_prompt = build_resume_review_prompt(resume_text, target_role)

    async for chunk in ai_client.stream_json(
        system_prompt=RESUME_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,
        max_tokens=1500,
    ):
        yield chunk
