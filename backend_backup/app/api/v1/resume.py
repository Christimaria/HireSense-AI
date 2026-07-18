"""
HireSense AI — Resume API Router
"""

import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.resume import ResumeReviewRequest
from app.services.resume_service import stream_resume_review
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/resume", tags=["Resume"])
logger = logging.getLogger(__name__)


@router.post(
    "/review",
    summary="Analyze a resume and return structured AI feedback",
    description=(
        "Accepts resume text (plain text) and an optional target role. "
        "Returns a Server-Sent Events stream of the AI-generated review. "
        "The final SSE event carries the complete JSON result. "
        "**Privacy**: Resume text is never stored or logged."
    ),
    response_description="SSE stream — final event contains full JSON review object",
)
async def review_resume(request: ResumeReviewRequest) -> StreamingResponse:
    """POST /api/v1/resume/review"""
    try:
        generator = stream_resume_review(
            resume_text=request.resume_text,
            target_role=request.target_role,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # Disable Nginx buffering for SSE
                "Connection": "keep-alive",
            },
        )
    except Exception as exc:
        logger.error("Resume review failed: %s", exc, exc_info=True)
        raise AIServiceError()
