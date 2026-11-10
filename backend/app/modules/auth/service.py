from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, verify_password
from backend.app.models.user import User
from backend.app.modules.auth.repository import AuthRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = AuthRepository(db)

    def login(self, email: str, password: str) -> tuple[str, User]:
        user = self.repo.find_user_by_email(email=email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        access_token = create_access_token(subject=user.id)
        return access_token, user

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.repo.find_user_by_id(user_id)

    @staticmethod
    def get_permissions(user: User) -> list[str]:
        permission_codes: set[str] = set()
        for role in user.roles:
            for permission in role.permissions:
                permission_codes.add(permission.code)
        return sorted(permission_codes)

