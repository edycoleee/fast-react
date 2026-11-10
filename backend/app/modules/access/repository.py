from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User


class AccessRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def count_users(self) -> int:
        return int(self.db.scalar(select(func.count(User.id))) or 0)

    def count_roles(self) -> int:
        return int(self.db.scalar(select(func.count(Role.id))) or 0)

    def count_permissions(self) -> int:
        return int(self.db.scalar(select(func.count(Permission.id))) or 0)
