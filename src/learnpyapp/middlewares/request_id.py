from __future__ import annotations

from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from learnpyapp.core.request_id import new_request_id, set_request_id


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    - Her request için request-id üretir (veya header’dan alır)
    - Response header’ına koyar
    - Loglara inject edebilmek için contextvar’a yazar
    """

    def __init__(self, app, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        rid = request.headers.get(self.header_name) or new_request_id()
        set_request_id(rid)

        response = await call_next(request)
        response.headers[self.header_name] = rid
        return response
