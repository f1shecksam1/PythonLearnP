# src/learnpyapp/middlewares/request_id.py
# 🌐 Her HTTP isteğine benzersiz bir X-Request-ID ekleyen middleware.

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, MutableMapping

from starlette.middleware.base import (
    BaseHTTPMiddleware,  # FastAPI'nin temel middleware sınıfı
)
from starlette.requests import Request
from starlette.responses import Response

from learnpyapp.core.request_id import new_request_id, set_request_id

# Starlette middleware tipleri (ASGIApp)
ASGIApp = Callable[
    [
        MutableMapping[str, Any],
        Callable[[], Awaitable[MutableMapping[str, Any]]],
        Callable[[MutableMapping[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]

# 🧠 Bu logger sadece HTTP istekleri için kullanılır
logger = logging.getLogger("learnpyapp.request")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    🎯 Amaç:
    - Her istek için request-id üretmek veya header’dan almak
    - Response’a X-Request-ID header’ı eklemek
    - Loglara request-id’yi işlemek
    """

    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # 🔍 Header’dan ID varsa kullan, yoksa yeni üret
        rid = request.headers.get(self.header_name) or new_request_id()
        set_request_id(rid)

        # 🚀 İstek başladığında log kaydı oluştur
        logger.info("➡️  %s %s [rid=%s]", request.method, request.url.path, rid)

        # İsteği devam ettir
        response = await call_next(request)

        # 🔚 İstek tamamlandığında log kaydı oluştur
        logger.info(
            "⬅️  %s %s %s [rid=%s]",
            request.method,
            request.url.path,
            response.status_code,
            rid,
        )

        # Response header’a X-Request-ID ekle
        response.headers[self.header_name] = rid
        return response
