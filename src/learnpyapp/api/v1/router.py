# src/learnpyapp/api/v1/router.py
from fastapi import APIRouter

from learnpyapp.api.v1.endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
