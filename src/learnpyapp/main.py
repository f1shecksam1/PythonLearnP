# src/learnpyapp/main.py
import logging

from fastapi import FastAPI

from learnpyapp.api.v1.router import api_router as v1_router
from learnpyapp.core.config import settings
from learnpyapp.core.logging import configure_logging
from learnpyapp.middlewares.request_id import RequestIdMiddleware


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting app: env=%s", settings.app_env)

    app = FastAPI(title=settings.app_name)

    # Middleware (request id)
    app.add_middleware(RequestIdMiddleware)

    # API v1
    app.include_router(v1_router, prefix="/api/v1")

    return app


app = create_app()
