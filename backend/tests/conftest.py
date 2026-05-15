"""테스트 공통 fixtures."""

import os

import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password


@pytest.fixture(autouse=True)
def env_setup():
    """테스트 환경변수 설정."""
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_EXPIRE_HOURS"] = "16"
    yield


@pytest.fixture(autouse=True)
def reset_db():
    """각 테스트 전 DB 초기화."""
    from app.core.storage import reset_all_tables
    reset_all_tables()
    yield
    reset_all_tables()


@pytest.fixture
def seed_data():
    """테스트용 시드 데이터 삽입."""
    from app.core.storage import get_table

    # AdminUser
    admin_table = get_table("AdminUser")
    admin_table.put_item(Item={
        "store_id": "store-001",
        "username": "admin",
        "password_hash": hash_password("admin1234"),
        "login_attempts": 0,
        "created_at": "2026-01-01T00:00:00Z",
    })

    # Table
    table_table = get_table("Table")
    table_table.put_item(Item={
        "store_id": "store-001",
        "table_id": "table-uuid-001",
        "table_number": 1,
        "password_hash": hash_password("1234"),
        "current_session_id": None,
        "created_at": "2026-01-01T00:00:00Z",
    })

    # TableSession (빈 상태)


@pytest.fixture
def client(seed_data):
    """FastAPI TestClient."""
    from app.main import app
    return TestClient(app)
