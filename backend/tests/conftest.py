import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.database import Base, get_db
from backend.app.core.security import hash_password
from backend.app.main import app
from backend.app.models.permission import Permission
from backend.app.models.role import Role
from backend.app.models.user import User

TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)


@pytest.fixture
def db_session() -> Session:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def seed_auth_data(db_session: Session) -> dict:
    access_read = Permission(code="access.read", description="read access summary")
    iam_manage = Permission(code="iam.manage", description="manage iam")
    db_session.add_all([access_read, iam_manage])
    db_session.flush()

    admin_role = Role(name="admin", description="administrator")
    admin_role.permissions = [access_read, iam_manage]
    viewer_role = Role(name="viewer", description="viewer")
    viewer_role.permissions = []
    db_session.add_all([admin_role, viewer_role])
    db_session.flush()

    admin_user = User(
        username="admin",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        is_active=True,
    )
    admin_user.roles = [admin_role]

    viewer_user = User(
        username="viewer",
        email="viewer@example.com",
        password_hash=hash_password("viewer123"),
        is_active=True,
    )
    viewer_user.roles = [viewer_role]

    db_session.add_all([admin_user, viewer_user])
    db_session.commit()

    return {
        "admin": {"email": "admin@example.com", "password": "admin123"},
        "viewer": {"email": "viewer@example.com", "password": "viewer123"},
    }


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_auth_headers(client: TestClient, seed_auth_data: dict) -> dict:
    response = client.post("/api/v1/auth/login", json=seed_auth_data["admin"])
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def viewer_auth_headers(client: TestClient, seed_auth_data: dict) -> dict:
    response = client.post("/api/v1/auth/login", json=seed_auth_data["viewer"])
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

