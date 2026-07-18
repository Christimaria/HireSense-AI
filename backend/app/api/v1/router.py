"""
HireSense AI — API v1 Router Aggregator
"""

from fastapi import APIRouter
from app.api.v1 import resume, interview, evaluation, roadmap

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(resume.router)
api_router.include_router(interview.router)
api_router.include_router(evaluation.router)
api_router.include_router(roadmap.router)
