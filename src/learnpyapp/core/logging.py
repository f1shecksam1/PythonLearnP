# src/learnpyapp/core/logging.py
from __future__ import annotations

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from learnpyapp.core.request_id import get_request_id


class RequestIdFilter(logging.Filter):
    """Her log kaydına request-id ekler."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging(level: str = "INFO", log_dir: str = "logs") -> None:
    """
    Gelişmiş logging yapılandırması:
    - Hem konsola hem dosyaya loglama
    - Günlük döngü (rotation)
    - Request-ID desteği
    """
    # Log klasörünü oluştur (yoksa)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    root = logging.getLogger()
    root.setLevel(level.upper())

    # Eski handler’ları temizle
    for h in list(root.handlers):
        root.removeHandler(h)

    # Log formatı
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s [%(name)s] [rid=%(request_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Konsol Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.upper())
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())

    # --- Dosya Handler (günlük rotation) ---
    file_handler = TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    file_handler.setLevel(level.upper())
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIdFilter())

    # Root logger’a ekle
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # Uvicorn logları da aynı seviyeye çek
    logging.getLogger("uvicorn").setLevel(level.upper())
    logging.getLogger("uvicorn.error").setLevel(level.upper())
    logging.getLogger("uvicorn.access").setLevel(level.upper())

    logging.getLogger(__name__).info("Logging configured. Log file: %s", log_path)
