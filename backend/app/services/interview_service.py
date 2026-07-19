"""
HireSense AI — Mock Interview Service

Stateless service layer that coordinates with the Google Gemini AI client
to generate and stream custom interview questions based on role, experience,
interview type, and previous session history.
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.interview_prompts import INTERVIEW_SYSTEM_PROMPT, build_question_prompt
from app.models.schemas.interview import ConversationTurn

logger = logging.getLogger(__name__)


async def stream_interview_question(
    role: str,
    experience_level: str,
    interview_type: str,
    question_number: int,
    total_questions: int,
    conversation_history: list[ConversationTurn],
) -> AsyncGenerator[str, None]:
    """
    Generate and stream raw text tokens for the next interview question.

    Converts the structured conversation history turns, constructs the custom prompt,
    and forwards streaming data from the Gemini model content generator.

    Args:
        role: Targeted job role (e.g., 'Software Engineer', 'Frontend').
        experience_level: Experience seniority level (e.g., 'Fresher', 'Junior').
        interview_type: Focus type of the interview (e.g., 'Technical', 'Behavioral').
        question_number: Index of the question to generate (1-indexed).
        total_questions: Total number of questions planned for the session.
        conversation_history: List of prior questions and candidate answers in this session.

    Yields:
        Raw text chunks from the Gemini stream.
    """
    logger.info(
        "Generating interview question | role=%r | exp=%r | type=%r | Q=%d/%d | history_len=%d",
        role,
        experience_level,
        interview_type,
        question_number,
        total_questions,
        len(conversation_history),
    )

    # Convert conversation turns into simple dictionary format expected by prompts
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

    # Use stream_text to yield raw text token streams
    async for chunk in ai_client.stream_text(
        system_prompt=INTERVIEW_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.7,  # Default temperature for diverse questions
        max_tokens=1024,
    ):
        yield chunk

    logger.info("Interview question generation stream complete | role=%r | Q=%d", role, question_number)
