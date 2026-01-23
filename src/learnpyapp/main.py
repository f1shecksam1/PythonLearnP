# src/learnpyapp/main.py
# 🧠 Bu dosya uygulamanın ana giriş noktasıdır.
# FastAPI uygulamasını oluşturur, gerekli ayarları ve middleware'leri ekler.

import logging  # Python'un yerleşik logging modülü, loglama işlemleri için kullanılır.

from fastapi import FastAPI  # FastAPI ana framework sınıfı (web app oluşturmak için).

# Proje içinden gerekli modülleri import ediyoruz:
from learnpyapp.api.v1.router import (
    api_router as v1_router,  # v1 API yönlendirmelerini alır.
)
from learnpyapp.core.config import (
    settings,  # Ortam değişkenlerinden gelen ayarları okur.
)
from learnpyapp.core.logging import configure_logging  # Loglama sistemini yapılandırır.
from learnpyapp.middlewares.request_id import (
    RequestIdMiddleware,  # Request-id ekleyen middleware.
)


def create_app() -> FastAPI:
    """
    🚀 Uygulama factory fonksiyonu (Factory Pattern)
    Her çağrıldığında yeni bir FastAPI uygulaması döndürür.
    Bu yöntem test edilebilirliği ve modülerliği artırır.
    """
    # 🔧 Logging sistemini başlat
    configure_logging(settings.log_level)

    # Ana logger nesnesini al (bu dosyadaki işlemleri loglayacağız)
    logger = logging.getLogger(__name__)
    logger.info("Starting app: env=%s", settings.app_env)  # Ortam bilgisini logla (örneğin: dev veya prod)

    # FastAPI uygulamasını oluştur (başlık bilgisiyle)
    app = FastAPI(title=settings.app_name)

    # 🧩 Middleware ekle: Her isteğe otomatik request-id ekler
    app.add_middleware(RequestIdMiddleware)

    # 🌐 API yönlendirmelerini ekle (v1 endpoints)
    app.include_router(v1_router, prefix="/api/v1")

    # FastAPI app nesnesini geri döndür
    return app


# 👇 Uygulama örneğini global olarak başlatıyoruz
# Uvicorn, bu değişkeni kullanarak app'i çalıştırır (örnek: uvicorn learnpyapp.main:app)
app = create_app()
