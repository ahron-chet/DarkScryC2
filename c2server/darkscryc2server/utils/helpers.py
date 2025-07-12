from __future__ import annotations

from typing import Any


def ensure_str(data: Any) -> str:
    """Return a string representation regardless of input type."""
    if isinstance(data, bytes):
        return data.decode()
    return str(data)
