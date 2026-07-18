"""
HireSense AI — Resume Review Pydantic Schemas
"""

from pydantic import BaseModel, Field, field_validator


class ResumeReviewRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=100,
        max_length=10_000,
        description="The plain text content of the resume.",
        examples=["John Doe\nSoftware Engineer with 3 years of experience..."],
    )
    target_role: str | None = Field(
        default=None,
        max_length=100,
        description="Optional target job role to tailor the feedback.",
        examples=["Frontend Developer"],
    )

    @field_validator("resume_text")
    @classmethod
    def strip_resume_text(cls, v: str) -> str:
        return v.strip()


class SectionFeedback(BaseModel):
    score: float = Field(..., ge=0, le=10)
    feedback: str


class ResumeReviewResponse(BaseModel):
    overall_score: float = Field(..., ge=0, le=10)
    ats_score: int = Field(..., ge=0, le=100, description="ATS compatibility score (0–100)")
    sections: dict[str, SectionFeedback]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
