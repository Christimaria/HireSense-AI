"""
HireSense AI — Diagnostic / Debug API Router (Temporary)

Exposes:
  GET /api/v1/debug/models
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.ai.client import _get_client

router = APIRouter(prefix="/debug", tags=["Debug Diagnostics"])
logger = logging.getLogger(__name__)


@router.get(
    "/models",
    summary="List available Gemini models for current API key",
    description="Queries Google GenAI SDK to retrieve all model IDs supporting generateContent.",
    status_code=200,
)
async def list_available_gemini_models():
    """
    GET /api/v1/debug/models
    Returns all models available to the configured API key that support generateContent.
    """
    try:
        client = _get_client()
        models_pager = client.models.list()
        models_list = list(models_pager)

        available_models = []
        flash_models = []

        for m in models_list:
            raw_name = getattr(m, "name", str(m))
            model_id = raw_name[7:] if raw_name.startswith("models/") else raw_name

            supported_methods = (
                getattr(m, "supported_generation_methods", None)
                or getattr(m, "supported_actions", None)
                or []
            )

            supports_gen = False
            if supported_methods:
                supports_gen = any("generateContent" in str(method) for method in supported_methods)
            else:
                supports_gen = any(k in model_id.lower() for k in ["flash", "pro", "gemini"])

            if supports_gen:
                available_models.append(model_id)
                if "flash" in model_id.lower():
                    flash_models.append(model_id)

        recommended = (
            flash_models[0]
            if flash_models
            else (available_models[0] if available_models else "gemini-1.5-flash")
        )

        return {
            "recommended": recommended,
            "available": available_models,
        }
    except Exception as exc:
        logger.error("Failed to query Gemini models list: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query Google GenAI models list: {exc}",
        )
