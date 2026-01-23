# src/learnpyapp/middlewares/request_id.py
from __future__ import annotations

import logging  # ✅ EKLENDİ
from typing import Any, Awaitable, Callable, MutableMapping

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from learnpyapp.core.request_id import new_request_id, set_request_id

# Starlette’in middleware fonksiyon tipi (daha doğru bir tahmin)
ASGIApp = Callable[
    [
        MutableMapping[str, Any],
        Callable[[], Awaitable[MutableMapping[str, Any]]],
        Callable[[MutableMapping[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]

# ✅ Global logger oluşturduk
logger = logging.getLogger("learnpyapp.request")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    - Her request için request-id üretir (veya header’dan alır)
    - Response header’ına koyar
    - Loglara inject edebilmek için contextvar’a yazar
    """

    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        rid = request.headers.get(self.header_name) or new_request_id()
        set_request_id(rid)

        # ✅ İstek öncesi log
        logger.info("➡️  %s %s [rid=%s]", request.method, request.url.path, rid)

        response = await call_next(request)

        # ✅ İstek sonrası log
        logger.info(
            "⬅️  %s %s %s [rid=%s]",
            request.method,
            request.url.path,
            response.status_code,
            rid,
        )

        response.headers[self.header_name] = rid
        return response
