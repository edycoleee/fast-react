from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.core.security import hash_password
from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User


def upsert_permission(db, code: str, description: str) -> Permission:
    permission = db.scalar(select(Permission).where(Permission.code == code))
    if permission:
        return permission
    permission = Permission(code=code, description=description)
    db.add(permission)
    db.flush()
    return permission


def upsert_role(db, name: str, description: str) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role:
        return role
    role = Role(name=name, description=description)
    db.add(role)
    db.flush()
    return role


def upsert_admin_user(db, role: Role) -> User:
    user = db.scalar(select(User).where(User.email == settings.seed_admin_email))
    if user:
        if role not in user.roles:
            user.roles.append(role)
        return user

    user = User(
        username=settings.seed_admin_username,
        email=settings.seed_admin_email,
        password_hash=hash_password(settings.seed_admin_password),
        is_active=True,
    )
    user.roles.append(role)
    db.add(user)
    db.flush()
    return user


def main() -> None:
    with SessionLocal() as db:
        access_permission = upsert_permission(
            db, code="access.read", description="Read access summary endpoint"
        )
        iam_permission = upsert_permission(
            db, code="iam.manage", description="Manage users, roles, and permissions"
        )
        admin_role = upsert_role(
            db, name="admin", description="Administrator with full boilerplate access"
        )
        if access_permission not in admin_role.permissions:
            admin_role.permissions.append(access_permission)
        if iam_permission not in admin_role.permissions:
            admin_role.permissions.append(iam_permission)

        user = upsert_admin_user(db, role=admin_role)
        db.commit()
        print(f"Seed completed. Admin email: {user.email}")


if __name__ == "__main__":
    main()
