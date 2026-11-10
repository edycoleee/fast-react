from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User


class IamRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _paginate(self, statement: Select, *, offset: int, limit: int) -> tuple[list, int]:
        total = int(
            self.db.scalar(
                select(func.count()).select_from(statement.order_by(None).subquery())
            )
            or 0
        )
        rows = list(self.db.scalars(statement.offset(offset).limit(limit)).all())
        return rows, total

    def list_permissions(
        self,
        *,
        q: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Permission], int]:
        statement = select(Permission)
        if q:
            pattern = f"%{q}%"
            statement = statement.where(
                Permission.code.ilike(pattern) | Permission.description.ilike(pattern)
            )
        statement = statement.order_by(Permission.code)
        return self._paginate(statement, offset=offset, limit=limit)

    def get_permission(self, permission_id: str) -> Permission | None:
        return self.db.get(Permission, permission_id)

    def add_permission(self, permission: Permission) -> Permission:
        self.db.add(permission)
        self.db.flush()
        return permission

    def delete_permission(self, permission: Permission) -> None:
        self.db.delete(permission)
        self.db.flush()

    def list_roles(
        self,
        *,
        q: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Role], int]:
        statement = select(Role)
        if q:
            pattern = f"%{q}%"
            statement = statement.where(
                Role.name.ilike(pattern) | Role.description.ilike(pattern)
            )
        statement = statement.order_by(Role.name)
        return self._paginate(statement, offset=offset, limit=limit)

    def get_role(self, role_id: str) -> Role | None:
        return self.db.get(Role, role_id)

    def add_role(self, role: Role) -> Role:
        self.db.add(role)
        self.db.flush()
        return role

    def delete_role(self, role: Role) -> None:
        self.db.delete(role)
        self.db.flush()

    def list_users(
        self,
        *,
        q: str | None,
        is_active: bool | None,
        offset: int,
        limit: int,
    ) -> tuple[list[User], int]:
        statement = select(User)
        if q:
            pattern = f"%{q}%"
            statement = statement.where(
                User.username.ilike(pattern) | User.email.ilike(pattern)
            )
        if is_active is not None:
            statement = statement.where(User.is_active == is_active)
        statement = statement.order_by(User.username)
        return self._paginate(statement, offset=offset, limit=limit)

    def get_user(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def add_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.flush()
