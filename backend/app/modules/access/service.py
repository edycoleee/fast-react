from sqlalchemy.orm import Session

from backend.app.modules.access.repository import AccessRepository


class AccessService:
    def __init__(self, db: Session) -> None:
        self.repo = AccessRepository(db)

    def summary(self) -> dict[str, int]:
        return {
            "users": self.repo.count_users(),
            "roles": self.repo.count_roles(),
            "permissions": self.repo.count_permissions(),
        }

