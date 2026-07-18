"""
HireSense AI — FastAPI Application Factory

Configures:
  - CORS middleware (environment-aware)
  - Rate limiting via SlowAPI
  - Structured JSON request logging
  - Global exception handlers
  - OpenAPI documentation (dev only)
  - All API routes
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import APIError, RateLimitError, APIConnectionError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.api.v1.router import api_router
from app.api.health import router as health_router

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("hiresense")


# ── Rate Limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["15/minute"])


# ── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle hooks."""
    settings = get_settings()
    logger.info(
        "HireSense AI starting | env=%s | model=%s",
        settings.environment,
        settings.openai_model,
    )
    yield
    logger.info("HireSense AI shutting down.")


# ── App Factory ────────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="HireSense AI",
        description=(
            "Intelligent Interview & Career Preparation Platform. "
            "Powered by GPT-4o with real-time SSE streaming responses."
        ),
        version="1.0.0",
        contact={
            "name": "HireSense AI",
            "url": "https://hiresense.ai",
        },
        # Hide docs in production
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Rate Limiter ──────────────────────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Accept", "X-Request-ID"],
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
    @app.exception_handler(RateLimitError)
    async def openai_rate_limit_handler(request: Request, exc: RateLimitError):
        logger.warning("OpenAI rate limit exceeded for %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "AI service is temporarily overloaded. Please try again in a moment."},
        )

    @app.exception_handler(APIConnectionError)
    async def openai_connection_handler(request: Request, exc: APIConnectionError):
        logger.error("OpenAI connection error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Could not reach AI service. Please check your connection."},
        )

    @app.exception_handler(APIError)
    async def openai_api_error_handler(request: Request, exc: APIError):
        logger.error("OpenAI API error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": "AI service returned an error. Please try again."},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
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
