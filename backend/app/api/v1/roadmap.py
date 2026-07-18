"""
HireSense AI — Career Roadmap API Router
"""

import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.roadmap import RoadmapRequest
from app.services.roadmap_service import stream_roadmap
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])
logger = logging.getLogger(__name__)


@router.post(
    "/generate",
    summary="Generate a personalized career learning roadmap",
    description=(
        "Accepts current skills, a target role, and a desired timeline. "
        "Returns a structured week-by-week career roadmap via SSE with: "
        "skill gap analysis, weekly focus areas, topics, curated resources, "
        "and concrete milestones."
    ),
    response_description="SSE stream — final event contains full roadmap JSON",
)
async def generate_roadmap(request: RoadmapRequest) -> StreamingResponse:
    """POST /api/v1/roadmap/generate"""
    try:
        generator = stream_roadmap(
            current_skills=request.current_skills,
            target_role=request.target_role,
            timeline_weeks=request.timeline_weeks,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )
    except Exception as exc:
        logger.error("Roadmap generation failed: %s", exc, exc_info=True)
        raise AIServiceError()
