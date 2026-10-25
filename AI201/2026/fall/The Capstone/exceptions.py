"""
Custom Exceptions and Error Envelopes for The Unofficial Guide (Shape B).

Provides structured domain exceptions and a standardized JSON error
response envelope for all bad-path conditions.
"""

from typing import Any


class CapstoneError(Exception):
    """Base class for all application domain exceptions."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class PayloadValidationError(CapstoneError):
    """Raised when client input fails boundary or format validation (HTTP 400)."""

    def __init__(self, message: str, code: str = "BAD_REQUEST"):
        super().__init__(message, code=code, status_code=400)


class VectorStoreUnavailableError(CapstoneError):
    """Raised when Chroma index is missing or corrupted (HTTP 503)."""

    def __init__(
        self,
        message: str = "Vector store index is not initialized. Run `python app.py index` to build it.",
        code: str = "INDEX_UNAVAILABLE",
    ):
        super().__init__(message, code=code, status_code=503)


class UpstreamModelTimeoutError(CapstoneError):
    """Raised when the generative AI provider times out (HTTP 504)."""

    def __init__(
        self,
        message: str = "Upstream model generation timed out.",
        code: str = "UPSTREAM_TIMEOUT",
    ):
        super().__init__(message, code=code, status_code=504)


def make_error_envelope(
    error: str,
    message: str,
    code: str,
    status_code: int,
    request_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a consistent, machine-readable JSON error envelope."""
    envelope = {
        "error": error,
        "message": message,
        "code": code,
        "status_code": status_code,
        "request_id": request_id,
    }
    if extra:
        envelope.update(extra)
    return envelope
