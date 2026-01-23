# src/learnpyapp/api/v1/endpoints/health.py
# 💓 Basit sağlık kontrolü endpoint’i (/api/v1/health)
# Sunucunun çalışıp çalışmadığını kontrol etmek için kullanılır.

from typing import Dict

from fastapi import APIRouter

# Router nesnesi oluştur (tag: health)
router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> Dict[str, str]:
    """
    🌡️ Sağlık kontrolü endpoint'i.
    Dış servisler (örneğin: load balancer) bu endpoint’i çağırarak
    uygulamanın çalıştığını doğrular.
    """
    return {"status": "ok"}  # Basit OK yanıtı
