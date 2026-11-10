from fastapi import APIRouter

from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.modules.access.router_api import router as access_router


def get_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(health_router)
    api_router.include_router(access_router, prefix="/api/v1")
    return api_router

