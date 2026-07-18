"""
HireSense AI — Career Roadmap Service
"""

import logging
from typing import AsyncGenerator

from app.ai import client as ai_client
from app.ai.prompts.roadmap_prompts import ROADMAP_SYSTEM_PROMPT, build_roadmap_prompt

logger = logging.getLogger(__name__)


async def stream_roadmap(
    current_skills: list[str],
    target_role: str,
    timeline_weeks: int,
) -> AsyncGenerator[str, None]:
    """
    Stream a personalized career roadmap as structured JSON.

    The roadmap identifies skill gaps between current skills and the target role,
    then generates a week-by-week learning plan with resources and milestones.
    """
    logger.info(
        "Generating career roadmap | target_role=%s | timeline=%d weeks | skills=%s",
        target_role,
        timeline_weeks,
        ", ".join(current_skills[:5]),  # Log first 5 skills only
    )

    user_prompt = build_roadmap_prompt(
        current_skills=current_skills,
        target_role=target_role,
        timeline_weeks=timeline_weeks,
    )

    async for chunk in ai_client.stream_json(
        system_prompt=ROADMAP_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.4,
        max_tokens=3000,   # Roadmaps can be verbose
    ):
        yield chunk
