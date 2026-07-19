"""
HireSense AI — Performance Dashboard Service

Stateless service layer that coordinates with the Google Gemini AI client
to analyze the full interview session turns and compute the performance dashboard.
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.dashboard_prompts import DASHBOARD_SYSTEM_PROMPT, build_dashboard_prompt
from app.models.schemas.interview import ConversationTurn

logger = logging.getLogger(__name__)


async def stream_dashboard_evaluation(
    role: str,
    experience_level: str,
    interview_type: str,
    session_turns: list[ConversationTurn],
) -> AsyncGenerator[str, None]:
    """
    Generate and stream raw JSON text chunks from Gemini for the holistic performance dashboard.

    Args:
        role: Targeted job role.
        experience_level: Experience seniority level.
        interview_type: Focus type of the interview.
        session_turns: List of all Q&A conversation turns completed in the session.

    Yields:
        Raw text chunks of the generated JSON output.
    """
    logger.info(
        "Generating performance dashboard | role=%r | exp=%r | type=%r | turns=%d",
        role,
        experience_level,
        interview_type,
        len(session_turns),
    )

    # Convert conversation turns to simple dictionaries
    turns_dicts = [
        {"question": turn.question, "answer": turn.answer}
        for turn in session_turns
    ]

    user_prompt = build_dashboard_prompt(
        role=role,
        experience_level=experience_level,
        interview_type=interview_type,
        session_turns=turns_dicts,
    )

    # Stream structured JSON
    async for chunk in ai_client.stream_json(
        system_prompt=DASHBOARD_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,  # Keep low for reliable formatting and analytical grading
        max_tokens=2048,
    ):
        yield chunk

    logger.info("Performance dashboard stream complete | role=%r", role)
