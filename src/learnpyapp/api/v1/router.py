# src/learnpyapp/api/v1/router.py
# 🌐 API v1 yönlendirmelerini birleştirir (router aggregator).

from fastapi import APIRouter

from learnpyapp.api.v1.endpoints.auth import router as auth_router

# Endpoint modülünü import et (örnek: /health)
from learnpyapp.api.v1.endpoints.health import router as health_router

# Ana API router’ı oluştur
api_router = APIRouter()

# Alt router’ı dahil et (örnek: /health)
api_router.include_router(health_router)
api_router.include_router(auth_router)
