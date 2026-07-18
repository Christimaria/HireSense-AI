"""
HireSense AI — Evaluation API Router

Two endpoints:
  POST /evaluation/answer    — Evaluate a single interview answer (SSE)
  POST /evaluation/dashboard — Generate full performance dashboard (SSE)
"""

import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas.evaluation import AnswerEvaluationRequest, DashboardRequest
from app.services.evaluation_service import (
    stream_answer_evaluation,
    stream_performance_dashboard,
)
from app.utils.sse import stream_json_object
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])
logger = logging.getLogger(__name__)

_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
    "Connection": "keep-alive",
}


@router.post(
    "/answer",
    summary="Evaluate a single interview answer",
    description=(
        "Accepts a question + candidate answer and returns a structured evaluation "
        "via SSE stream: score (0–10), strengths, weaknesses, an improved model answer, "
        "and actionable interview tips."
    ),
    response_description="SSE stream — final event contains full evaluation JSON",
)
async def evaluate_answer(request: AnswerEvaluationRequest) -> StreamingResponse:
    """POST /api/v1/evaluation/answer"""
    try:
        generator = stream_answer_evaluation(
            role=request.role.value,
            interview_type=request.interview_type.value,
            experience_level=request.experience_level.value,
            question=request.question,
            answer=request.answer,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Answer evaluation failed: %s", exc, exc_info=True)
        raise AIServiceError()


@router.post(
    "/dashboard",
    summary="Generate a comprehensive post-interview performance dashboard",
    description=(
        "Accepts all Q&A pairs from a completed interview session. "
        "Returns a structured performance dashboard via SSE with: "
        "overall score, category-wise scores, top strengths, key weaknesses, "
        "prioritized improvement areas, recommended study topics, "
        "interview readiness assessment, and concrete next steps."
    ),
    response_description="SSE stream — final event contains full dashboard JSON",
)
async def generate_dashboard(request: DashboardRequest) -> StreamingResponse:
    """POST /api/v1/evaluation/dashboard"""
    try:
        generator = stream_performance_dashboard(
            role=request.role.value,
            interview_type=request.interview_type.value,
            experience_level=request.experience_level.value,
            session=request.session,
        )
        return StreamingResponse(
            stream_json_object(generator),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )
    except Exception as exc:
        logger.error("Dashboard generation failed: %s", exc, exc_info=True)
        raise AIServiceError()
