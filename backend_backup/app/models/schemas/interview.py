"""
HireSense AI — Interview Pydantic Schemas
"""

from enum import Enum
from pydantic import BaseModel, Field


class InterviewRole(str, Enum):
    SOFTWARE_ENGINEER = "Software Engineer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    BACKEND_DEVELOPER = "Backend Developer"
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    DATA_ANALYST = "Data Analyst"
    DATA_SCIENTIST = "Data Scientist"
    AI_ENGINEER = "AI Engineer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    CYBERSECURITY_ANALYST = "Cybersecurity Analyst"
    HR_INTERVIEW = "HR Interview"


class InterviewType(str, Enum):
    TECHNICAL = "Technical"
    BEHAVIORAL = "Behavioral"
    HR = "HR"


class ExperienceLevel(str, Enum):
    FRESHER = "Fresher"
    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"


class ConversationTurn(BaseModel):
    """A single Q&A exchange in the interview history."""
    question: str
    answer: str


class InterviewQuestionRequest(BaseModel):
    role: InterviewRole
    experience_level: ExperienceLevel
    interview_type: InterviewType
    question_number: int = Field(..., ge=1, le=20)
    total_questions: int = Field(default=10, ge=1, le=20)
    conversation_history: list[ConversationTurn] = Field(
        default_factory=list,
        description="All previous Q&A turns in this session.",
    )
