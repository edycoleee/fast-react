from fastapi import FastAPI

from backend.app.api.router import get_api_router
from backend.app.core.config import settings
from backend.app.core.errors import register_exception_handlers

app = FastAPI(title=settings.app_name)
register_exception_handlers(app)
app.include_router(get_api_router())

