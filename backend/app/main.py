"""
HireSense AI — FastAPI Application Factory

Configures:
  - CORS middleware (environment-aware)
  - Structured request logging
  - Global exception handlers
  - Health endpoint (/health)
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.api.health import router as health_router
from app.api.v1.router import api_router

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("hiresense")


# ── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle hooks."""
    settings = get_settings()
    logger.info(
        "HireSense AI starting | env=%s | resolved_gemini_model=%s",
        settings.environment,
        settings.gemini_model,
    )
    yield
    logger.info("HireSense AI shutting down.")


# ── App Factory ────────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="HireSense AI",
        description=(
            "Intelligent Interview & Career Preparation Platform."
        ),
        version="1.0.0",
        contact={
            "name": "HireSense AI",
            "url": "https://hiresense.ai",
        },
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Type"],
    )

    # ── Request logging middleware ────────────────────────────────────────────
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s | status=%d | %.1fms | ip=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request.client.host if request.client else "unknown",
        )
        return response

    # ── Global Exception Handlers ─────────────────────────────────────────────
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        error_str = str(exc).lower()
        if "429" in error_str or "resource_exhausted" in error_str:
            logger.warning("Gemini rate limit exceeded for %s", request.url.path)
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "AI service is temporarily overloaded. Please try again in a moment."},
            )
        if "connection" in error_str or "timeout" in error_str:
            logger.error("AI service connection error: %s", exc)
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Could not reach AI service. Please check your connection."},
            )
        logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred. Please try again."},
        )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(health_router)       # /health, /ready
    app.include_router(api_router)          # /api/v1/...

    return app


# ── Entry point ───────────────────────────────────────────────────────────────
app = create_app()
