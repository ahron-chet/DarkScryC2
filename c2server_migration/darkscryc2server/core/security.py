from __future__ import annotations

from fastapi import HTTPException, status


def verify_token(token: str, expected: str) -> None:
    """Simple token verification used by API routes."""
    if token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
