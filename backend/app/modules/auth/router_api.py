from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.modules.auth.dependencies import get_current_user
from backend.app.modules.auth.schemas import LoginRequest
from backend.app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    token, user = AuthService(db).login(email=payload.email, password=payload.password)
    permissions = AuthService.get_permissions(user)
    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "permissions": permissions,
            },
        },
        "meta": None,
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    permissions = AuthService.get_permissions(current_user)
    return {
        "success": True,
        "message": "Current user fetched",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "permissions": permissions,
        },
        "meta": None,
    }

