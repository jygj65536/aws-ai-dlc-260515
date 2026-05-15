"""auth_service 단위 테스트."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.core.security import hash_password
from app.services import auth_service


class TestAdminLogin:
    """관리자 로그인 테스트."""

    def test_admin_login_success(self):
        """정상 로그인 시 토큰을 반환한다."""
        mock_admin = {
            "store_id": "store-001",
            "username": "admin",
            "password_hash": hash_password("admin1234"),
            "login_attempts": 0,
        }
        with patch(
            "app.services.auth_service.admin_user_repository.get_by_username",
            return_value=mock_admin,
        ):
            with patch(
                "app.services.auth_service.admin_user_repository.reset_login_attempts"
            ):
                result = auth_service.admin_login("store-001", "admin", "admin1234")

        assert "access_token" in result
        assert result["token_type"] == "bearer"

    def test_admin_login_wrong_password(self):
        """잘못된 비밀번호 시 401을 반환한다."""
        mock_admin = {
            "store_id": "store-001",
            "username": "admin",
            "password_hash": hash_password("admin1234"),
            "login_attempts": 0,
        }
        with patch(
            "app.services.auth_service.admin_user_repository.get_by_username",
            return_value=mock_admin,
        ):
            with patch(
                "app.services.auth_service.admin_user_repository.update_login_attempts"
            ):
                with pytest.raises(HTTPException) as exc_info:
                    auth_service.admin_login("store-001", "admin", "wrong")

        assert exc_info.value.status_code == 401

    def test_admin_login_user_not_found(self):
        """존재하지 않는 사용자 시 401을 반환한다."""
        with patch(
            "app.services.auth_service.admin_user_repository.get_by_username",
            return_value=None,
        ):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.admin_login("store-001", "nobody", "pass")

        assert exc_info.value.status_code == 401

    def test_admin_login_account_locked(self):
        """계정 잠금 상태에서 423을 반환한다."""
        future_time = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        mock_admin = {
            "store_id": "store-001",
            "username": "admin",
            "password_hash": hash_password("admin1234"),
            "login_attempts": 5,
            "locked_until": future_time,
        }
        with patch(
            "app.services.auth_service.admin_user_repository.get_by_username",
            return_value=mock_admin,
        ):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.admin_login("store-001", "admin", "admin1234")

        assert exc_info.value.status_code == 423

    def test_admin_login_5th_failure_locks_account(self):
        """5회 연속 실패 시 계정을 잠근다."""
        mock_admin = {
            "store_id": "store-001",
            "username": "admin",
            "password_hash": hash_password("admin1234"),
            "login_attempts": 4,  # 이번이 5번째 실패
        }
        with patch(
            "app.services.auth_service.admin_user_repository.get_by_username",
            return_value=mock_admin,
        ):
            with patch(
                "app.services.auth_service.admin_user_repository.lock_account"
            ) as mock_lock:
                with pytest.raises(HTTPException) as exc_info:
                    auth_service.admin_login("store-001", "admin", "wrong")

        assert exc_info.value.status_code == 423
        mock_lock.assert_called_once()


class TestTableLogin:
    """테이블 로그인 테스트."""

    def test_table_login_success_no_session(self):
        """정상 로그인 시 토큰과 null session_id를 반환한다."""
        mock_table = {
            "store_id": "store-001",
            "table_id": "table-uuid-001",
            "table_number": 1,
            "password_hash": hash_password("1234"),
            "current_session_id": None,
        }
        with patch(
            "app.services.auth_service.table_repository.get_by_table_number",
            return_value=mock_table,
        ):
            result = auth_service.table_login("store-001", 1, "1234")

        assert "access_token" in result
        assert result["table_id"] == "table-uuid-001"
        assert result["session_id"] is None

    def test_table_login_success_with_active_session(self):
        """활성 세션이 있으면 session_id를 반환한다."""
        mock_table = {
            "store_id": "store-001",
            "table_id": "table-uuid-001",
            "table_number": 1,
            "password_hash": hash_password("1234"),
            "current_session_id": "session-001",
        }
        mock_session = {
            "table_id": "table-uuid-001",
            "session_id": "session-001",
            "status": "active",
        }
        with patch(
            "app.services.auth_service.table_repository.get_by_table_number",
            return_value=mock_table,
        ):
            with patch(
                "app.services.auth_service.session_repository.get_active_session",
                return_value=mock_session,
            ):
                result = auth_service.table_login("store-001", 1, "1234")

        assert result["session_id"] == "session-001"

    def test_table_login_wrong_password(self):
        """잘못된 비밀번호 시 401을 반환한다."""
        mock_table = {
            "store_id": "store-001",
            "table_id": "table-uuid-001",
            "table_number": 1,
            "password_hash": hash_password("1234"),
        }
        with patch(
            "app.services.auth_service.table_repository.get_by_table_number",
            return_value=mock_table,
        ):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.table_login("store-001", 1, "wrong")

        assert exc_info.value.status_code == 401

    def test_table_login_table_not_found(self):
        """존재하지 않는 테이블 시 401을 반환한다."""
        with patch(
            "app.services.auth_service.table_repository.get_by_table_number",
            return_value=None,
        ):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.table_login("store-001", 99, "1234")

        assert exc_info.value.status_code == 401
