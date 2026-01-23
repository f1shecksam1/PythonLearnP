# src/learnpyapp/middlewares/request_id_middleware.py
# 🌐 Her HTTP isteğine benzersiz bir X-Request-ID ekleyen middleware.

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, MutableMapping

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from learnpyapp.core.request_id import new_request_id, set_request_id

# ASGI tip tanımı
ASGIApp = Callable[
    [
        MutableMapping[str, Any],
        Callable[[], Awaitable[MutableMapping[str, Any]]],
        Callable[[MutableMapping[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]

logger = logging.getLogger("learnpyapp.request")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    🎯 Amaç:
    - Her istek için request-id üretmek veya header’dan almak
    - Response’a X-Request-ID header’ı eklemek
    - Loglara request-id’yi işlemek
    """

    def __init__(
        self: "RequestIdMiddleware", app: ASGIApp, header_name: str = "X-Request-ID"
    ) -> None:
        super().__init__(app)
        self.header_name = header_name  # ✅ artık self tipi doğru sınıf

    async def dispatch(
        self: "RequestIdMiddleware",
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        rid = request.headers.get(self.header_name) or new_request_id()
        set_request_id(rid)

        logger.info("➡️  %s %s [rid=%s]", request.method, request.url.path, rid)

        response = await call_next(request)

        logger.info(
            "⬅️  %s %s %s [rid=%s]",
            request.method,
            request.url.path,
            response.status_code,
            rid,
        )

        response.headers[self.header_name] = rid
        return response
