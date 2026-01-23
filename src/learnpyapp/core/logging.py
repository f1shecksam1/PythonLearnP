# src/learnpyapp/core/logging.py
# 🧠 Gelişmiş loglama sistemi
# - Konsola ve dosyaya loglama
# - Günlük döngüsü (rotation)
# - Request-ID desteği

from __future__ import annotations

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from learnpyapp.core.request_id import (
    get_request_id,  # Log kayıtlarına request-id eklemek için
)


class RequestIdFilter(logging.Filter):
    """🔗 Her log kaydına request-id ekleyen özel filter sınıfı."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Log kaydına request-id alanı ekler
        record.request_id = get_request_id()
        return True


def configure_logging(level: str = "INFO", log_dir: str = "logs") -> None:
    """
    🧱 Loglama sistemini yapılandırır.
    - Konsol ve dosya çıktısı
    - Günlük rotasyonu (TimedRotatingFileHandler)
    - Request-ID filtreleme
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)  # Log klasörü yoksa oluştur
    log_path = os.path.join(log_dir, "app.log")

    # Ana logger (root) al
    root = logging.getLogger()
    root.setLevel(level.upper())

    # Eski handler’ları temizle (yeniden başlatırken tekrar eklenmesin)
    for h in list(root.handlers):
        root.removeHandler(h)

    # 📜 Log formatı (tarih, seviye, isim, request-id)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s [%(name)s] [rid=%(request_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 🖥️ Konsol handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.upper())
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())

    # 📁 Dosya handler (günlük rotasyonu)
    file_handler = TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    file_handler.setLevel(level.upper())
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIdFilter())

    # Handler’ları root logger’a ekle
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # ⚙️ Uvicorn loglarını da root’a yönlendir
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []  # Varsayılan handler’ları temizle
        uvicorn_logger.propagate = True  # Root’a gönder
        uvicorn_logger.setLevel(level.upper())

    # Bilgi logu
    logging.getLogger(__name__).info("Logging configured → %s", log_path)
