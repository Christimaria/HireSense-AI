"""
HireSense AI — Evaluation Pydantic Schemas
"""

from pydantic import BaseModel, Field
from app.models.schemas.interview import InterviewRole, InterviewType, ExperienceLevel


# ── Single Answer Evaluation ──────────────────────────────────────────────────

class AnswerEvaluationRequest(BaseModel):
    role: InterviewRole
    interview_type: InterviewType
    experience_level: ExperienceLevel
    question: str = Field(..., min_length=5, max_length=2000)
    answer: str = Field(..., min_length=1, max_length=5000)


class AnswerEvaluationResponse(BaseModel):
    score: float = Field(..., ge=0, le=10)
    strengths: list[str]
    weaknesses: list[str]
    improved_answer: str
    tips: list[str]


# ── Performance Dashboard ─────────────────────────────────────────────────────

class SessionQA(BaseModel):
    """One Q&A entry with its pre-computed evaluation score."""
    question_number: int
    question: str
    answer: str
    score: float = Field(..., ge=0, le=10)
    category: str = Field(
        default="General",
        description="Topic category of the question (e.g., 'JavaScript', 'System Design').",
    )


class DashboardRequest(BaseModel):
    role: InterviewRole
    interview_type: InterviewType
    experience_level: ExperienceLevel
    session: list[SessionQA] = Field(..., min_length=1)


class ImprovementArea(BaseModel):
    area: str
    priority: str  # High | Medium | Low
    suggestion: str


class StudyResource(BaseModel):
    topic: str
    resource: str
    url: str | None = None


class DashboardResponse(BaseModel):
    overall_score: float
    performance_grade: str  # Excellent | Good | Average | Needs Improvement
    category_scores: dict[str, float]
    top_strengths: list[str]
    key_weaknesses: list[str]
    improvement_areas: list[ImprovementArea]
    recommended_topics: list[StudyResource]
    interview_readiness: str
    next_steps: list[str]
