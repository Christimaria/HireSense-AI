"""
HireSense AI — Career Roadmap Pydantic Schemas
"""

from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    current_skills: list[str] = Field(
        ...,
        min_length=1,
        description="List of skills the user already has.",
        examples=[["Python", "SQL", "Excel"]],
    )
    target_role: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="The role the user wants to transition into.",
        examples=["Data Scientist"],
    )
    timeline_weeks: int = Field(
        default=12,
        ge=4,
        le=52,
        description="Desired timeline in weeks (4–52).",
    )


class RoadmapResource(BaseModel):
    title: str
    url: str | None = None
    type: str  # free | paid | book | youtube


class RoadmapWeek(BaseModel):
    week_range: str          # e.g., "1-2"
    focus: str               # e.g., "Mathematics & Statistics"
    topics: list[str]
    resources: list[RoadmapResource]
    milestone: str


class RoadmapResponse(BaseModel):
    roadmap_title: str
    skill_gaps: list[str]
    weeks: list[RoadmapWeek]
