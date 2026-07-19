"""
HireSense AI — Career Roadmap API Router

Exposes:
  POST /api/v1/roadmap/generate
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.roadmap import RoadmapRequest
from app.services.roadmap_service import stream_roadmap_generation
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/roadmap", tags=["Career Roadmap"])
logger = logging.getLogger(__name__)

# Standard SSE headers — prevent buffering at every layer of the stack
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",   # Disable Nginx proxy buffering
    "Connection": "keep-alive",
}


@router.post(
    "/generate",
    summary="Generate a customized week-by-week learning roadmap and stream structured feedback",
    description=(
        "Accepts current skills, target role, and timeline. "
        "Returns a **Server-Sent Events (SSE)** stream. "
        "\n\n**SSE event types:**\n"
        "- `chunk` — incremental JSON text from Gemini\n"
        "- `result` — final parsed `RoadmapResponse` JSON object\n"
        "- `error` — error payload if the AI call fails\n"
        "- `[DONE]` — stream terminator"
    ),
    response_description="SSE stream — consume `result` event for the full customized career roadmap.",
    status_code=200,
)
async def generate_career_roadmap(request: RoadmapRequest) -> StreamingResponse:
    """
    POST /api/v1/roadmap/generate

    Returns an SSE StreamingResponse. The client should listen for:
      data: {"type": "chunk",  "content": "<partial JSON>"}
      data: {"type": "result", "content": { ...RoadmapResponse... }}
      data: [DONE]
    """
    try:
        generator = stream_roadmap_generation(
            current_skills=request.current_skills,
            target_role=request.target_role,
            timeline=request.timeline,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Career roadmap endpoint error: %s", exc, exc_info=True)
        raise AIServiceError()
