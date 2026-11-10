import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault(
    "DB_URL", "postgresql+psycopg://fast_boiler:fast_boiler@localhost:5432/fast_boiler_test"
)

from backend.app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

