from __future__ import annotations

import logging

from learnpyapp.core.request_id import get_request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging(level: str = "INFO") -> None:
    """
    Basit ama üretimde iş gören bir logging setup:
    - request_id log formatına eklenir
    - root logger seviyelendirilir
    """
    root = logging.getLogger()
    root.setLevel(level.upper())

    # Eski handler’ları temizlemek (reload vb. durumlarda çakışmasın)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler()
    handler.setLevel(level.upper())
    handler.addFilter(RequestIdFilter())

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] [rid=%(request_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)

    # Uvicorn logları da aynı seviyeye çekilsin
    logging.getLogger("uvicorn").setLevel(level.upper())
    logging.getLogger("uvicorn.error").setLevel(level.upper())
    logging.getLogger("uvicorn.access").setLevel(level.upper())
