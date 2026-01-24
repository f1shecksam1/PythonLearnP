# src/learnpyapp/core/logging.py
# 🧠 Gelişmiş loglama sistemi
# - Konsola ve dosyaya loglama
# - Günlük döngüsü (rotation)
# - Request-ID desteği

from __future__ import annotations

import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from learnpyapp.core.request_id import get_request_id


class RequestIdFilter(logging.Filter):
    def filter(self: logging.Filter, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging(level: str = "INFO", log_dir: str = "logs") -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    root = logging.getLogger()
    root.setLevel(level.upper())

    for h in list(root.handlers):
        root.removeHandler(h)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s [%(name)s] [rid=%(request_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.upper())
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())

    # ---- burada: TimedRotatingFileHandler + özel isimlendirme ----
    file_handler = TimedRotatingFileHandler(
        log_path,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(level.upper())
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIdFilter())

    # default: app.log.2026-01-24  ->  hedef: app2026-01-24.log
    _default_pat = re.compile(r"^(?P<base>.+)\.log\.(?P<date>\d{4}-\d{2}-\d{2})$")

    def _namer(default_name: str) -> str:
        folder, fname = os.path.split(default_name)
        m = _default_pat.match(fname)
        if not m:
            return default_name
        return os.path.join(folder, f"{m.group('base')}{m.group('date')}.log")

    file_handler.namer = _namer

    # backupCount eski logları silebilsin diye yeni pattern’e göre extMatch
    base_prefix = Path(log_path).stem  # "app"
    file_handler.extMatch = re.compile(
        rf"^{re.escape(base_prefix)}\d{{4}}-\d{{2}}-\d{{2}}\.log$"
    )
    # -------------------------------------------------------------

    root.addHandler(console_handler)
    root.addHandler(file_handler)

    for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True
        uvicorn_logger.setLevel(level.upper())

    logging.getLogger(__name__).info("Logging configured → %s", log_path)
