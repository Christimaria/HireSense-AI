"""
HireSense AI — Mock Interview Evaluation Service

Stateless service layer that coordinates with the Google Gemini AI client
to grade a candidate's response to an interview question and suggest improvements.
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.evaluation_prompts import EVALUATION_SYSTEM_PROMPT, build_evaluation_prompt

logger = logging.getLogger(__name__)


async def stream_evaluation(
    question: str,
    answer: str,
    role: str,
    experience_level: str,
    interview_type: str,
) -> AsyncGenerator[str, None]:
    """
    Generate and stream raw JSON text chunks from Gemini for grading a candidate's answer.

    Args:
        question: The interview question asked.
        answer: The candidate's response.
        role: Targeted job role.
        experience_level: Experience seniority level.
        interview_type: Focus type of the interview.

    Yields:
        Raw text chunks of the generated JSON output.
    """
    logger.info(
        "Evaluating candidate answer | role=%r | exp=%r | type=%r | question_len=%d | answer_len=%d",
        role,
        experience_level,
        interview_type,
        len(question),
        len(answer),
    )

    user_prompt = build_evaluation_prompt(
        question=question,
        answer=answer,
        role=role,
        experience_level=experience_level,
        interview_type=interview_type,
    )

    # Use stream_json for clean, structured JSON model outputs
    async for chunk in ai_client.stream_json(
        system_prompt=EVALUATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,  # Low temperature for strict, stable scoring and formatting
        max_tokens=2048,
    ):
        yield chunk

    logger.info("Answer evaluation stream complete | role=%r", role)
