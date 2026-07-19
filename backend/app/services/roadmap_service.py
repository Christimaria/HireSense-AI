"""
HireSense AI — Career Roadmap Service

Stateless service layer that coordinates with the Google Gemini AI client
to generate a week-by-week personalized learning pathway.
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.roadmap_prompts import ROADMAP_SYSTEM_PROMPT, build_roadmap_prompt

logger = logging.getLogger(__name__)


async def stream_roadmap_generation(
    current_skills: list[str],
    target_role: str,
    timeline: str,
) -> AsyncGenerator[str, None]:
    """
    Generate and stream raw JSON text chunks from Gemini for a custom career roadmap.

    Args:
        current_skills: List of candidate's existing skills.
        target_role: Target job title.
        timeline: Expected timeframe for training.

    Yields:
        Raw text chunks of the generated JSON output.
    """
    logger.info(
        "Generating career roadmap | target_role=%r | timeline=%r | skills_count=%d",
        target_role,
        timeline,
        len(current_skills),
    )

    user_prompt = build_roadmap_prompt(
        current_skills=current_skills,
        target_role=target_role,
        timeline=timeline,
    )

    # Use stream_json for structured, clean JSON models
    async for chunk in ai_client.stream_json(
        system_prompt=ROADMAP_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.4,  # Moderate temperature to balance structured format with planning creativity
        max_tokens=4096,
    ):
        yield chunk

    logger.info("Career roadmap stream complete | target_role=%r", target_role)
