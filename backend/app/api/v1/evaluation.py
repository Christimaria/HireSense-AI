"""
HireSense AI — Interview Evaluation API Router

Exposes:
  POST /api/v1/evaluation/answer
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.evaluation import EvaluationRequest, DashboardRequest
from app.services.evaluation_service import stream_evaluation
from app.services.dashboard_service import stream_dashboard_evaluation
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/evaluation", tags=["Interview Evaluation"])
logger = logging.getLogger(__name__)

# Standard SSE headers — prevent buffering at every layer of the stack
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",   # Disable Nginx proxy buffering
    "Connection": "keep-alive",
}


@router.post(
    "/answer",
    summary="Evaluate candidate answer and stream structured feedback",
    description=(
        "Accepts the question, candidate's answer, role, experience level, and interview type. "
        "Returns a **Server-Sent Events (SSE)** stream. "
        "\n\n**SSE event types:**\n"
        "- `chunk` — incremental JSON text from Gemini\n"
        "- `result` — final parsed `EvaluationResponse` JSON object\n"
        "- `error` — error payload if the AI call fails\n"
        "- `[DONE]` — stream terminator"
    ),
    response_description="SSE stream — consume `result` event for the full structured evaluation.",
    status_code=200,
)
async def evaluate_candidate_answer(request: EvaluationRequest) -> StreamingResponse:
    """
    POST /api/v1/evaluation/answer

    Returns an SSE StreamingResponse. The client should listen for:
      data: {"type": "chunk",  "content": "<partial JSON>"}
      data: {"type": "result", "content": { ...EvaluationResponse... }}
      data: [DONE]
    """
    try:
        generator = stream_evaluation(
            question=request.question,
            answer=request.answer,
            role=request.role.value,
            experience_level=request.experience_level.value,
            interview_type=request.interview_type.value,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Answer evaluation endpoint error: %s", exc, exc_info=True)
        raise AIServiceError()


@router.post(
    "/dashboard",
    summary="Generate holistic interview performance dashboard and stream structured analysis",
    description=(
        "Accepts the role, experience level, interview type, and all conversation turns in the session. "
        "Returns a **Server-Sent Events (SSE)** stream. "
        "\n\n**SSE event types:**\n"
        "- `chunk` — incremental JSON text from Gemini\n"
        "- `result` — final parsed `DashboardResponse` JSON object\n"
        "- `error` — error payload if the AI call fails\n"
        "- `[DONE]` — stream terminator"
    ),
    response_description="SSE stream — consume `result` event for the complete performance dashboard analysis.",
    status_code=200,
)
async def generate_performance_dashboard(request: DashboardRequest) -> StreamingResponse:
    """
    POST /api/v1/evaluation/dashboard

    Returns an SSE StreamingResponse. The client should listen for:
      data: {"type": "chunk",  "content": "<partial JSON>"}
      data: {"type": "result", "content": { ...DashboardResponse... }}
      data: [DONE]
    """
    try:
        generator = stream_dashboard_evaluation(
            role=request.role.value,
            experience_level=request.experience_level.value,
            interview_type=request.interview_type.value,
            session_turns=request.session_turns,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Performance dashboard endpoint error: %s", exc, exc_info=True)
        raise AIServiceError()
