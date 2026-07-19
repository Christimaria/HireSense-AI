"""
HireSense AI — Resume Review API Router

Exposes:
  POST /api/v1/resume/review

The endpoint is intentionally thin — it validates the request, delegates
to the service, and wraps the async generator with the SSE helper.
All business logic lives in the service and AI layers.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.resume import ResumeReviewRequest
from app.services.resume_service import stream_resume_review
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/resume", tags=["Resume Review"])
logger = logging.getLogger(__name__)

# Standard SSE headers — prevent buffering at every layer of the stack
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",   # Disable Nginx proxy buffering
    "Connection": "keep-alive",
}


@router.post(
    "/review",
    summary="Analyse a resume and stream structured AI feedback",
    description=(
        "Accepts the candidate's resume as plain text and an optional target role. "
        "Returns a **Server-Sent Events (SSE)** stream. "
        "\n\n**SSE event types:**\n"
        "- `chunk` — incremental JSON text from Gemini (use for typing animation)\n"
        "- `result` — final parsed `ResumeReviewResponse` JSON object\n"
        "- `error` — error payload if the AI call fails\n"
        "- `[DONE]` — stream terminator\n\n"
        "**Privacy:** resume text is never stored or persisted."
    ),
    response_description="SSE stream — consume `result` event for the full analysis.",
    status_code=200,
)
async def review_resume(request: ResumeReviewRequest) -> StreamingResponse:
    """
    POST /api/v1/resume/review

    Returns an SSE StreamingResponse. The client should listen for:
      data: {"type": "chunk",  "content": "<partial JSON>"}
      data: {"type": "result", "content": { ...ResumeReviewResponse... }}
      data: [DONE]
    """
    try:
        generator = stream_resume_review(
            resume_text=request.resume_text,
            target_role=request.target_role,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Resume review endpoint error: %s", exc, exc_info=True)
        raise AIServiceError()
