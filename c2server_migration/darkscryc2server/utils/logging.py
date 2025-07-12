"""Logging utilities for the C2 server."""

from __future__ import annotations

import json
import logging
import os
from typing import Any


class JsonFormatter(logging.Formatter):
    """Simple JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - formatting
        data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(data)


def setup_logging() -> None:
    """Configure root logging for the application."""

    env_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = logging.getLevelName(env_level)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger following the project configuration."""

    return logging.getLogger(name)
