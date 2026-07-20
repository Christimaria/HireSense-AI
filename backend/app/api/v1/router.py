"""
HireSense AI — API v1 Router Aggregator

All feature routers are imported and registered here.
main.py includes this single api_router under /api/v1.
"""

from fastapi import APIRouter

from app.api.v1 import resume
from app.api.v1 import interview
from app.api.v1 import evaluation
from app.api.v1 import roadmap
from app.api.v1 import debug

api_router = APIRouter(prefix="/api/v1")

# ── Feature routers ────────────────────────────────────────────────────────────
api_router.include_router(resume.router)      # POST /api/v1/resume/review
api_router.include_router(interview.router)   # POST /api/v1/interview/question
api_router.include_router(evaluation.router)  # POST /api/v1/evaluation/answer
api_router.include_router(roadmap.router)     # POST /api/v1/roadmap/generate
api_router.include_router(debug.router)       # GET /api/v1/debug/models
