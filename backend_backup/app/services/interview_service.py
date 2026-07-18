"""
HireSense AI — Interview Question Service
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.interview_prompts import (
    INTERVIEW_SYSTEM_PROMPT,
    build_question_prompt,
)
from app.models.schemas.interview import ConversationTurn

logger = logging.getLogger(__name__)


async def stream_next_question(
    role: str,
    experience_level: str,
    interview_type: str,
    question_number: int,
    total_questions: int,
    conversation_history: list[ConversationTurn],
) -> AsyncGenerator[str, None]:
    """
    Stream the next interview question as plain text tokens.

    The conversation_history sent by the frontend makes this endpoint fully
    stateless — no server-side session tracking required.
    """
    logger.info(
        "Generating question %d/%d | role=%s | type=%s | level=%s",
        question_number,
        total_questions,
        role,
        interview_type,
        experience_level,
    )

    # Convert Pydantic models to plain dicts for the prompt builder
    history_dicts = [
        {"question": turn.question, "answer": turn.answer}
        for turn in conversation_history
    ]

    user_prompt = build_question_prompt(
        role=role,
        experience_level=experience_level,
        interview_type=interview_type,
        question_number=question_number,
        total_questions=total_questions,
        conversation_history=history_dicts,
    )

    async for chunk in ai_client.stream_text(
        system_prompt=INTERVIEW_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.75,   # Slight variety so questions feel fresh
        max_tokens=512,
    ):
        yield chunk
