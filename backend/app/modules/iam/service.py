from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.core.security import hash_password
from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User
from backend.app.modules.iam.repository import IamRepository


def _permission_to_dict(permission: Permission) -> dict:
    return {
        "id": permission.id,
        "code": permission.code,
        "description": permission.description,
    }


def _role_to_dict(role: Role) -> dict:
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "permissions": [_permission_to_dict(permission) for permission in role.permissions],
    }


def _user_to_dict(user: User) -> dict:
    permissions = sorted(
        {
            permission.code
            for role in user.roles
            for permission in role.permissions
        }
    )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "roles": [{"id": role.id, "name": role.name} for role in user.roles],
        "permissions": permissions,
    }


class IamService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = IamRepository(db)

    @staticmethod
    def _pagination_meta(*, page: int, page_size: int, total: int, q: str | None) -> dict:
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "q": q or "",
        }

    def list_permissions(
        self,
        *,
        page: int,
        page_size: int,
        q: str | None,
    ) -> tuple[list[dict], dict]:
        offset = (page - 1) * page_size
        permissions, total = self.repo.list_permissions(q=q, offset=offset, limit=page_size)
        data = [_permission_to_dict(permission) for permission in permissions]
        meta = self._pagination_meta(page=page, page_size=page_size, total=total, q=q)
        return data, meta

    def create_permission(self, code: str, description: str | None) -> dict:
        permission = Permission(code=code.strip(), description=description)
        try:
            self.repo.add_permission(permission)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Permission code already exists",
            ) from exc
        return _permission_to_dict(permission)

    def update_permission(self, permission_id: str, code: str | None, description: str | None) -> dict:
        permission = self.repo.get_permission(permission_id)
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        if code is not None:
            permission.code = code.strip()
        if description is not None:
            permission.description = description
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Permission code already exists",
            ) from exc
        self.db.refresh(permission)
        return _permission_to_dict(permission)

    def delete_permission(self, permission_id: str) -> None:
        permission = self.repo.get_permission(permission_id)
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        if permission.roles:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Permission still assigned to roles",
            )
        self.repo.delete_permission(permission)
        self.db.commit()

    def list_roles(
        self,
        *,
        page: int,
        page_size: int,
        q: str | None,
    ) -> tuple[list[dict], dict]:
        offset = (page - 1) * page_size
        roles, total = self.repo.list_roles(q=q, offset=offset, limit=page_size)
        data = [_role_to_dict(role) for role in roles]
        meta = self._pagination_meta(page=page, page_size=page_size, total=total, q=q)
        return data, meta

    def create_role(self, name: str, description: str | None, permission_ids: list[str]) -> dict:
        permissions = []
        for permission_id in permission_ids:
            permission = self.repo.get_permission(permission_id)
            if not permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Permission not found: {permission_id}",
                )
            permissions.append(permission)
        role = Role(name=name.strip(), description=description)
        role.permissions = permissions
        try:
            self.repo.add_role(role)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists") from exc
        self.db.refresh(role)
        return _role_to_dict(role)

    def update_role(
        self,
        role_id: str,
        name: str | None,
        description: str | None,
        permission_ids: list[str] | None,
    ) -> dict:
        role = self.repo.get_role(role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        if name is not None:
            role.name = name.strip()
        if description is not None:
            role.description = description
        if permission_ids is not None:
            permissions = []
            for permission_id in permission_ids:
                permission = self.repo.get_permission(permission_id)
                if not permission:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Permission not found: {permission_id}",
                    )
                permissions.append(permission)
            role.permissions = permissions
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists") from exc
        self.db.refresh(role)
        return _role_to_dict(role)

    def delete_role(self, role_id: str) -> None:
        role = self.repo.get_role(role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        if role.users:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role still assigned to users",
            )
        self.repo.delete_role(role)
        self.db.commit()

    def list_users(
        self,
        *,
        page: int,
        page_size: int,
        q: str | None,
        is_active: bool | None,
    ) -> tuple[list[dict], dict]:
        offset = (page - 1) * page_size
        users, total = self.repo.list_users(
            q=q,
            is_active=is_active,
            offset=offset,
            limit=page_size,
        )
        data = [_user_to_dict(user) for user in users]
        meta = self._pagination_meta(page=page, page_size=page_size, total=total, q=q)
        meta["is_active"] = is_active
        return data, meta

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role_ids: list[str],
        is_active: bool,
    ) -> dict:
        roles = []
        for role_id in role_ids:
            role = self.repo.get_role(role_id)
            if not role:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role not found: {role_id}")
            roles.append(role)
        user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password),
            is_active=is_active,
        )
        user.roles = roles
        try:
            self.repo.add_user(user)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists",
            ) from exc
        self.db.refresh(user)
        return _user_to_dict(user)

    def update_user(
        self,
        user_id: str,
        username: str | None,
        email: str | None,
        password: str | None,
        role_ids: list[str] | None,
        is_active: bool | None,
    ) -> dict:
        user = self.repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if username is not None:
            user.username = username.strip()
        if email is not None:
            user.email = email.strip().lower()
        if password is not None:
            user.password_hash = hash_password(password)
        if role_ids is not None:
            roles = []
            for role_id in role_ids:
                role = self.repo.get_role(role_id)
                if not role:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Role not found: {role_id}",
                    )
                roles.append(role)
            user.roles = roles
        if is_active is not None:
            user.is_active = is_active
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists",
            ) from exc
        self.db.refresh(user)
        return _user_to_dict(user)

    def delete_user(self, user_id: str) -> None:
        user = self.repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.repo.delete_user(user)
        self.db.commit()
