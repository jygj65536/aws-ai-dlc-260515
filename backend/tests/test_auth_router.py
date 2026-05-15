"""auth router 통합 테스트."""

from unittest.mock import patch

import pytest

from app.core.security import create_access_token, hash_password


class TestAdminLoginEndpoint:
    """POST /api/auth/admin/login 테스트."""

    def test_admin_login_success(self, client):
        """정상 로그인 시 200 + 토큰 반환."""
        response = client.post(
            "/api/auth/admin/login",
            json={
                "store_id": "store-001",
                "username": "admin",
                "password": "admin1234",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_admin_login_wrong_password(self, client):
        """잘못된 비밀번호 시 401 반환."""
        response = client.post(
            "/api/auth/admin/login",
            json={
                "store_id": "store-001",
                "username": "admin",
                "password": "wrongpass",
            },
        )
        assert response.status_code == 401

    def test_admin_login_user_not_found(self, client):
        """존재하지 않는 사용자 시 401 반환."""
        response = client.post(
            "/api/auth/admin/login",
            json={
                "store_id": "store-001",
                "username": "nobody",
                "password": "pass",
            },
        )
        assert response.status_code == 401


class TestTableLoginEndpoint:
    """POST /api/auth/table/login 테스트."""

    def test_table_login_success(self, client):
        """정상 로그인 시 200 + 토큰 + table_id 반환."""
        response = client.post(
            "/api/auth/table/login",
            json={
                "store_id": "store-001",
                "table_number": 1,
                "password": "1234",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["table_id"] == "table-uuid-001"
        assert data["session_id"] is None

    def test_table_login_wrong_password(self, client):
        """잘못된 비밀번호 시 401 반환."""
        response = client.post(
            "/api/auth/table/login",
            json={
                "store_id": "store-001",
                "table_number": 1,
                "password": "wrong",
            },
        )
        assert response.status_code == 401

    def test_table_login_table_not_found(self, client):
        """존재하지 않는 테이블 시 401 반환."""
        response = client.post(
            "/api/auth/table/login",
            json={
                "store_id": "store-001",
                "table_number": 99,
                "password": "1234",
            },
        )
        assert response.status_code == 401


class TestMeEndpoint:
    """GET /api/auth/me 테스트."""

    def test_me_admin(self, client):
        """관리자 토큰으로 인증 정보 확인."""
        token = create_access_token(
            data={"store_id": "store-001", "username": "admin", "role": "admin"}
        )
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_type"] == "admin"
        assert data["store_id"] == "store-001"
        assert data["user_id"] == "admin"
        assert data["table_id"] is None

    def test_me_table(self, client):
        """테이블 토큰으로 인증 정보 확인."""
        token = create_access_token(
            data={"store_id": "store-001", "table_id": "table-uuid-001", "role": "table"}
        )
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_type"] == "table"
        assert data["table_id"] == "table-uuid-001"
        assert data["user_id"] is None

    def test_me_no_token(self, client):
        """토큰 없이 요청 시 401/403 반환."""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # HTTPBearer returns 403 when no token
