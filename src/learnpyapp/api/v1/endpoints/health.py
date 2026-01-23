# src/learnpyapp/api/v1/endpoints/health.py
from typing import Dict

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> Dict[str, str]:  # ✅ return type eklendi
    return {"status": "ok"}
