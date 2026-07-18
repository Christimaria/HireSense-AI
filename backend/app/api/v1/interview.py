"""
HireSense AI — Interview API Router
"""

import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.interview import InterviewQuestionRequest
from app.services.interview_service import stream_next_question
from app.utils.sse import stream_text_chunks
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/interview", tags=["Interview"])
logger = logging.getLogger(__name__)


@router.post(
    "/question",
    summary="Generate the next interview question",
    description=(
        "Stateless endpoint — the frontend sends the complete conversation history "
        "on every call. The AI generates the next contextually relevant question "
        "based on the role, experience level, interview type, and previous Q&A pairs. "
        "Returns a token-by-token SSE stream of the question text."
    ),
    response_description="SSE stream of question text tokens",
)
async def get_next_question(request: InterviewQuestionRequest) -> StreamingResponse:
    """POST /api/v1/interview/question"""
    try:
        generator = stream_next_question(
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
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )
    except Exception as exc:
        logger.error("Interview question generation failed: %s", exc, exc_info=True)
        raise AIServiceError()
