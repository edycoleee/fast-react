from fastapi import APIRouter

from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.modules.access.router_api import router as access_router
from backend.app.modules.auth.router_api import router as auth_router
from backend.app.modules.iam.router_api import router as iam_router


def get_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(health_router)
    api_router.include_router(auth_router, prefix="/api/v1")
    api_router.include_router(access_router, prefix="/api/v1")
    api_router.include_router(iam_router, prefix="/api/v1")
    return api_router
