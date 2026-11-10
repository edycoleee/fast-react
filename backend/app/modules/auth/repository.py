from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def find_user_by_id(self, user_id: str) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

