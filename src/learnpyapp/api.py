import logging

from fastapi import FastAPI

from learnpyapp.core.config import settings
from learnpyapp.core.logging import configure_logging
from learnpyapp.middlewares.request_id import RequestIdMiddleware
from learnpyapp.routers import health_router


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting app: env=%s", settings.app_env)

    app = FastAPI(title=settings.app_name)

    # Middleware (request id)
    app.add_middleware(RequestIdMiddleware)

    # Routers
    app.include_router(health_router)

    return app


app = create_app()
