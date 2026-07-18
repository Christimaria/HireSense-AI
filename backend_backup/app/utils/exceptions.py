"""
HireSense AI — Custom HTTP Exceptions
"""

from fastapi import HTTPException, status


class InvalidResumeError(HTTPException):
    def __init__(self, detail: str = "Invalid resume input."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class AIServiceError(HTTPException):
    def __init__(self, detail: str = "AI service is temporarily unavailable. Please try again."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class RateLimitError(HTTPException):
    def __init__(self, detail: str = "Too many requests. Please slow down."):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)


class ValidationError(HTTPException):
    def __init__(self, detail: str = "Request validation failed."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
