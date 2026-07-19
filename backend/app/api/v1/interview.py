"""
HireSense AI — Mock Interview API Router

Exposes:
  POST /api/v1/interview/question
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.interview import InterviewQuestionRequest
from app.services.interview_service import stream_interview_question
from app.utils.sse import stream_text_chunks
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/interview", tags=["Mock Interview"])
logger = logging.getLogger(__name__)

# Standard SSE headers — prevent buffering at every layer of the stack
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",   # Disable Nginx proxy buffering
    "Connection": "keep-alive",
}


@router.post(
    "/question",
    summary="Generate next mock interview question and stream content",
    description=(
        "Accepts interview config (role, experience level, interview type, etc.) and history. "
        "Returns a **Server-Sent Events (SSE)** stream of raw question text. "
        "\n\n**SSE event types:**\n"
        "- `chunk` — incremental text from Gemini\n"
        "- `error` — error payload if the AI call fails\n"
        "- `[DONE]` — stream terminator"
    ),
    response_description="SSE stream — consume `chunk` events to read the generated question.",
    status_code=200,
)
async def get_interview_question(request: InterviewQuestionRequest) -> StreamingResponse:
    """
    POST /api/v1/interview/question

    Returns an SSE StreamingResponse of plain text chunks for the next interview question.
    """
    try:
        generator = stream_interview_question(
            role=request.role.value,
            experience_level=request.experience_level.value,
            interview_type=request.interview_type.value,
            question_number=request.question_number,
            total_questions=request.total_questions,
            conversation_history=request.conversation_history,
        )
        return StreamingResponse(
            stream_text_chunks(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Interview question endpoint error: %s", exc, exc_info=True)
        raise AIServiceError()
