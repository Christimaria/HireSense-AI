"""
HireSense AI — Health Check Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@router.get(
    "/health",
    summary="Liveness probe",
    description="Returns 200 OK if the service is running. Used by Docker and AWS App Runner.",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="HireSense AI API", version="1.0.0")


@router.get(
    "/ready",
    summary="Readiness probe",
    description="Returns 200 OK when the service is ready to accept traffic.",
    response_model=HealthResponse,
)
async def ready() -> HealthResponse:
    return HealthResponse(status="ready", service="HireSense AI API", version="1.0.0")
