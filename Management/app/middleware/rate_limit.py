from collections import deque
from time import monotonic
from typing import Deque, Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, max_requests: int, window: int) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self._requests: Dict[str, Deque[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = monotonic()
        queue = self._requests.setdefault(client_ip, deque())
        while queue and now - queue[0] > self.window:
            queue.popleft()
        if len(queue) >= self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        queue.append(now)
        return await call_next(request)
