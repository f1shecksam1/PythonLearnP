# src/learnpyapp/core/request_id.py
# 🔑 Her HTTP isteğine benzersiz bir Request-ID eklemek için yardımcı modül.

from __future__ import annotations

import contextvars  # Thread-safe context değişkenleri için
import uuid  # Unique ID üretmek için

# 🧠 Her request'e özel context değişkeni
_request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


def get_request_id() -> str:
    """🔍 Aktif request’in request-id değerini döndürür."""
    return _request_id_ctx.get()


def set_request_id(value: str) -> None:
    """✏️ Mevcut request context’ine yeni ID atar."""
    _request_id_ctx.set(value)


def new_request_id() -> str:
    """🆕 Rastgele yeni bir request-id (UUID) oluşturur."""
    return uuid.uuid4().hex
