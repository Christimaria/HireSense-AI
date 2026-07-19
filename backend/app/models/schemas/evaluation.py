"""
HireSense AI — Interview Evaluation Pydantic Schemas

Request
───────
  EvaluationRequest   POST body accepted by POST /api/v1/evaluation/answer

Response (parsed from the SSE `result` event by the frontend)
─────────────────────────────────────────────────────────────
  EvaluationResponse  Full structured JSON feedback returned by Gemini
"""

from pydantic import BaseModel, Field, field_validator
from app.models.schemas.interview import InterviewRole, ExperienceLevel, InterviewType, ConversationTurn


class EvaluationRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="The interview question that was asked of the candidate.",
        examples=["Explain event delegation in JavaScript and why it is useful."],
    )
    answer: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="The candidate's response to the question.",
        examples=["Event delegation is a technique where you attach a single listener to a parent element..."],
    )
    role: InterviewRole = Field(
        ...,
        description="Target job role to tailor evaluation criteria.",
    )
    experience_level: ExperienceLevel = Field(
        ...,
        description="Experience seniority level to tailor evaluation expectations.",
    )
    interview_type: InterviewType = Field(
        ...,
        description="Focus type of the interview.",
    )

    @field_validator("question", "answer")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class EvaluationResponse(BaseModel):
    score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Float score evaluating the answer quality on a scale of 0 to 10.",
    )
    strengths: list[str] = Field(
        ...,
        description="3-5 positive elements or correct technical details in the candidate's answer.",
    )
    weaknesses: list[str] = Field(
        ...,
        description="3-5 gaps, inaccuracies, or areas of improvement in the candidate's answer.",
    )
    improved_answer: str = Field(
        ...,
        description="A comprehensive, model answer showing how the candidate should have answered.",
    )
    tips: list[str] = Field(
        ...,
        description="3-5 general tips or advice for answering this specific style of question.",
    )


class DashboardRequest(BaseModel):
    role: InterviewRole = Field(
        ...,
        description="Target job role of the mock interview session.",
    )
    experience_level: ExperienceLevel = Field(
        ...,
        description="Experience seniority level of the candidate.",
    )
    interview_type: InterviewType = Field(
        ...,
        description="Type of the interview session.",
    )
    session_turns: list[ConversationTurn] = Field(
        ...,
        min_items=1,
        description="All Q&A exchanges completed in this interview session.",
    )


class DashboardResponse(BaseModel):
    overall_score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Holistic float score evaluating the candidate's performance across the session.",
    )
    category_scores: dict[str, float] = Field(
        ...,
        description="Breakdown of performance scores in categories like Technical Depth, Communication, Problem Solving, etc.",
    )
    performance_grade: str = Field(
        ...,
        description="Overall grade representing the performance (e.g., A, B+, C-).",
    )
    strengths: list[str] = Field(
        ...,
        description="3-5 key candidate strengths demonstrated during the interview.",
    )
    weaknesses: list[str] = Field(
        ...,
        description="3-5 candidate gaps or areas of minor competence demonstrated during the interview.",
    )
    improvement_areas: list[str] = Field(
        ...,
        description="Specific technical topics or soft skills areas that need active learning/practice.",
    )
    interview_readiness: str = Field(
        ...,
        description="An honest assessment of the candidate's preparedness to face real interviews.",
    )
    next_steps: list[str] = Field(
        ...,
        description="3-5 concrete, actionable roadmap items for the candidate's preparation.",
    )
