"""
HireSense AI — Career Roadmap Pydantic Schemas

Request
───────
  RoadmapRequest   POST body accepted by POST /api/v1/roadmap/generate

Response (parsed from the SSE `result` event by the frontend)
─────────────────────────────────────────────────────────────
  RoadmapResponse  Full structured JSON feedback returned by Gemini
"""

from pydantic import BaseModel, Field, field_validator


class RoadmapRequest(BaseModel):
    current_skills: list[str] = Field(
        ...,
        min_items=1,
        description="List of candidate's current skills or technologies they already know.",
        examples=[["HTML", "CSS", "Basic JavaScript"]],
    )
    target_role: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="The target job role the candidate wants to transition to.",
        examples=["Frontend Developer"],
    )
    timeline: str = Field(
        ...,
        min_length=2,
        max_length=60,
        description="The desired timeframe for this roadmap, e.g., '3 months' or '8 weeks'.",
        examples=["3 months"],
    )

    @field_validator("target_role", "timeline")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class WeeklyPlan(BaseModel):
    week: int = Field(..., description="Week index (e.g. 1, 2, 3...)")
    focus: str = Field(..., description="The primary goal or topic of focus for this week.")
    topics: list[str] = Field(..., description="Specific sub-topics to learn or research.")
    tasks: list[str] = Field(..., description="Hands-on tasks or practical project steps to complete.")


class ResourceItem(BaseModel):
    title: str = Field(..., description="Name of the resource.")
    url: str | None = Field(default=None, description="Optional link to access the resource online.")
    type: str = Field(..., description="Type of the resource (e.g., Course, Documentation, Book, Tutorial).")
    description: str = Field(..., description="Brief explanation of why this resource is useful.")


class MilestoneItem(BaseModel):
    week_number: int = Field(..., description="The week number when this milestone should be achieved.")
    title: str = Field(..., description="Title of the milestone check.")
    description: str = Field(..., description="Success criteria or definition of done for the milestone.")


class RoadmapResponse(BaseModel):
    weekly_roadmap: list[WeeklyPlan] = Field(..., description="Array of week-by-week focus and tasks.")
    skill_gaps: list[str] = Field(..., description="Identified core skill gaps between current skills and target role.")
    learning_resources: list[ResourceItem] = Field(..., description="Recommended learning resources.")
    milestones: list[MilestoneItem] = Field(..., description="Checkpoints to verify learning and project progress.")
