import logging.config

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.celery import create_celery
from app.core.config import EnvironmentType, settings
from app.core.sentry import init_sentry
from app.exceptions_handlers import install_exception_handlers
from app.healthcheck.debug import mount_debug_endpoints
from app.middlewares import add_cors_middleware

logging.config.fileConfig(settings.LOGGING_CONF_FILE, disable_existing_loggers=False)

print("SETUP -> Setting up the app")
app = FastAPI(title=settings.PROJECT_NAME)
celery_app = create_celery()

add_cors_middleware(app)
install_exception_handlers(app)

print("SETUP -> Connecting routers")
app.include_router(api_router, prefix=settings.API_V1_STR)

if settings.DEBUG:
    print("SETUP -> Mounting debug endpoints")
    mount_debug_endpoints(app)

if settings.ENVIRONMENT is not EnvironmentType.LOCAL:
    print("SETUP -> Configuring observsability tools")
    init_sentry()
else:
    print("SETUP -> Skipping observsability tools")
