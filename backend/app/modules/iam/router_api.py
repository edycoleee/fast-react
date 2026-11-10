from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.modules.auth.dependencies import require_permission
from backend.app.modules.iam.schemas import (
    PermissionCreateRequest,
    PermissionUpdateRequest,
    RoleCreateRequest,
    RoleUpdateRequest,
    UserCreateRequest,
    UserUpdateRequest,
)
from backend.app.modules.iam.service import IamService

router = APIRouter(prefix="/iam", tags=["iam"])


@router.get("/permissions")
def list_permissions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, max_length=120),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data, meta = IamService(db).list_permissions(page=page, page_size=page_size, q=q)
    return {"success": True, "message": "Permissions fetched", "data": data, "meta": meta}


@router.post("/permissions", status_code=status.HTTP_201_CREATED)
def create_permission(
    payload: PermissionCreateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).create_permission(code=payload.code, description=payload.description)
    return {"success": True, "message": "Permission created", "data": data, "meta": None}


@router.patch("/permissions/{permission_id}")
def update_permission(
    permission_id: str,
    payload: PermissionUpdateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).update_permission(
        permission_id=permission_id,
        code=payload.code,
        description=payload.description,
    )
    return {"success": True, "message": "Permission updated", "data": data, "meta": None}


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> None:
    IamService(db).delete_permission(permission_id=permission_id)


@router.get("/roles")
def list_roles(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, max_length=120),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data, meta = IamService(db).list_roles(page=page, page_size=page_size, q=q)
    return {"success": True, "message": "Roles fetched", "data": data, "meta": meta}


@router.post("/roles", status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).create_role(
        name=payload.name,
        description=payload.description,
        permission_ids=payload.permission_ids,
    )
    return {"success": True, "message": "Role created", "data": data, "meta": None}


@router.patch("/roles/{role_id}")
def update_role(
    role_id: str,
    payload: RoleUpdateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).update_role(
        role_id=role_id,
        name=payload.name,
        description=payload.description,
        permission_ids=payload.permission_ids,
    )
    return {"success": True, "message": "Role updated", "data": data, "meta": None}


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> None:
    IamService(db).delete_role(role_id=role_id)


@router.get("/users")
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, max_length=120),
    is_active: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data, meta = IamService(db).list_users(
        page=page,
        page_size=page_size,
        q=q,
        is_active=is_active,
    )
    return {"success": True, "message": "Users fetched", "data": data, "meta": meta}


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).create_user(
        username=payload.username,
        email=str(payload.email),
        password=payload.password,
        role_ids=payload.role_ids,
        is_active=payload.is_active,
    )
    return {"success": True, "message": "User created", "data": data, "meta": None}


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> dict:
    data = IamService(db).update_user(
        user_id=user_id,
        username=payload.username,
        email=str(payload.email) if payload.email else None,
        password=payload.password,
        role_ids=payload.role_ids,
        is_active=payload.is_active,
    )
    return {"success": True, "message": "User updated", "data": data, "meta": None}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("iam.manage")),
) -> None:
    IamService(db).delete_user(user_id=user_id)
