"""
HireSense AI — Resume Review Pydantic Schemas

Request
───────
  ResumeReviewRequest   POST body accepted by POST /api/v1/resume/review

Response (parsed from the SSE `result` event by the frontend)
─────────────────────────────────────────────────────────────
  SectionFeedback       Per-section score + feedback string
  ResumeReviewResponse  Full structured analysis returned by Gemini
"""

from pydantic import BaseModel, Field, field_validator


class ResumeReviewRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=100,
        max_length=10_000,
        description="Plain-text content of the candidate's resume.",
        examples=["Jane Smith\nSoftware Engineer — 5 years Python/FastAPI experience..."],
    )
    target_role: str | None = Field(
        default=None,
        max_length=120,
        description="Optional target job title to tailor the AI's feedback.",
        examples=["Senior Backend Engineer"],
    )

    @field_validator("resume_text")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 100:
            raise ValueError("resume_text must be at least 100 characters after stripping whitespace.")
        return stripped


# ── Response models (used for OpenAPI docs; actual streaming is via SSE) ──────

class SectionFeedback(BaseModel):
    score: float = Field(..., ge=0.0, le=10.0, description="Section quality score (0–10).")
    feedback: str = Field(..., description="Concise, actionable feedback for this section.")


class ResumeReviewResponse(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=10.0, description="Holistic resume quality score (0–10).")
    ats_score: int = Field(..., ge=0, le=100, description="ATS keyword/format compatibility score (0–100).")
    sections: dict[str, SectionFeedback] = Field(
        ...,
        description="Per-section breakdown: summary, experience, skills, education.",
    )
    strengths: list[str] = Field(..., description="3–5 notable strengths of this resume.")
    weaknesses: list[str] = Field(..., description="3–5 areas that need improvement.")
    recommendations: list[str] = Field(..., description="3–5 specific, actionable recommendations.")
