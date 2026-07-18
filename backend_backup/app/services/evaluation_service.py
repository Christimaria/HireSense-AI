"""
HireSense AI — Evaluation Service

Handles two distinct evaluation concerns:
  1. Single-answer evaluation (score, strengths, weaknesses, improved answer, tips)
  2. Post-interview performance dashboard (aggregated analysis across all Q&A pairs)
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.evaluation_prompts import (
    EVALUATION_SYSTEM_PROMPT,
    DASHBOARD_SYSTEM_PROMPT,
    build_evaluation_prompt,
    build_dashboard_prompt,
)
from app.models.schemas.evaluation import SessionQA

logger = logging.getLogger(__name__)


async def stream_answer_evaluation(
    role: str,
    interview_type: str,
    experience_level: str,
    question: str,
    answer: str,
) -> AsyncGenerator[str, None]:
    """
    Stream a structured evaluation of a single interview answer.
    Returns JSON with score, strengths, weaknesses, improved_answer, and tips.
    """
    logger.info(
        "Evaluating answer | role=%s | type=%s | level=%s | answer_length=%d",
        role,
        interview_type,
        experience_level,
        len(answer),
    )

    user_prompt = build_evaluation_prompt(
        role=role,
        interview_type=interview_type,
        experience_level=experience_level,
        question=question,
        answer=answer,
    )

    async for chunk in ai_client.stream_json(
        system_prompt=EVALUATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,
        max_tokens=1024,
    ):
        yield chunk


async def stream_performance_dashboard(
    role: str,
    interview_type: str,
    experience_level: str,
    session: list[SessionQA],
) -> AsyncGenerator[str, None]:
    """
    Stream a comprehensive performance dashboard for a completed interview session.
    Aggregates all Q&A pairs into category scores, strengths/weaknesses,
    improvement areas, and study recommendations.
    """
    logger.info(
        "Generating performance dashboard | role=%s | type=%s | total_questions=%d",
        role,
        interview_type,
        len(session),
    )

    # Convert Pydantic models to plain dicts for the prompt builder
    session_dicts = [
        {
            "question_number": qa.question_number,
            "question": qa.question,
            "answer": qa.answer,
            "score": qa.score,
            "category": qa.category,
        }
        for qa in session
    ]

    user_prompt = build_dashboard_prompt(
        role=role,
        interview_type=interview_type,
        experience_level=experience_level,
        session_data=session_dicts,
    )

    async for chunk in ai_client.stream_json(
        system_prompt=DASHBOARD_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,
        max_tokens=2048,
    ):
        yield chunk
