"""인증 서비스 (비즈니스 로직)."""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repositories import admin_user_repository, session_repository, table_repository

# 비즈니스 규칙 상수
MAX_LOGIN_ATTEMPTS = 5
LOCK_DURATION_MINUTES = 15


def admin_login(store_id: str, username: str, password: str) -> dict:
    """관리자 로그인을 처리한다.

    비즈니스 규칙:
    - AUTH-01: 연속 5회 실패 시 15분 계정 잠금
    - AUTH-02: JWT 16시간 만료

    Args:
        store_id: 매장 ID
        username: 사용자명
        password: 평문 비밀번호

    Returns:
        {"access_token": str, "token_type": "bearer"}

    Raises:
        HTTPException: 401 (잘못된 자격증명), 423 (계정 잠금)
    """
    # 1. AdminUser 조회
    admin_user = admin_user_repository.get_by_username(store_id, username)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 자격증명입니다",
        )

    # 2. 계정 잠금 확인
    locked_until = admin_user.get("locked_until")
    if locked_until:
        lock_time = datetime.fromisoformat(locked_until)
        if datetime.now(timezone.utc) < lock_time:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="계정이 잠겨있습니다. 잠시 후 다시 시도해주세요",
            )

    # 3. 비밀번호 검증
    if not verify_password(password, admin_user["password_hash"]):
        # 실패 처리
        attempts = admin_user.get("login_attempts", 0) + 1
        if attempts >= MAX_LOGIN_ATTEMPTS:
            # 계정 잠금
            locked_until_time = datetime.now(timezone.utc) + timedelta(
                minutes=LOCK_DURATION_MINUTES
            )
            admin_user_repository.lock_account(
                store_id, username, locked_until_time.isoformat()
            )
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="로그인 시도 횟수를 초과하여 계정이 잠겼습니다",
            )
        else:
            admin_user_repository.update_login_attempts(store_id, username, attempts)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 자격증명입니다",
            )

    # 4. 성공: 시도 횟수 초기화 + JWT 생성
    admin_user_repository.reset_login_attempts(store_id, username)
    token = create_access_token(
        data={
            "store_id": store_id,
            "username": username,
            "role": "admin",
        }
    )
    return {"access_token": token, "token_type": "bearer"}


def table_login(store_id: str, table_number: int, password: str) -> dict:
    """테이블 태블릿 로그인을 처리한다.

    비즈니스 규칙:
    - AUTH-03: JWT 16시간 만료
    - 활성 세션 확인 후 session_id 반환 (없으면 null)

    Args:
        store_id: 매장 ID
        table_number: 테이블 번호
        password: 테이블 비밀번호

    Returns:
        {"access_token": str, "table_id": str, "session_id": str|None}

    Raises:
        HTTPException: 401 (잘못된 자격증명)
    """
    # 1. Table 조회 (GSI: TableNumberIndex)
    table = table_repository.get_by_table_number(store_id, table_number)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 자격증명입니다",
        )

    # 2. 비밀번호 검증
    if not verify_password(password, table["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 자격증명입니다",
        )

    # 3. JWT 생성
    table_id = table["table_id"]
    token = create_access_token(
        data={
            "store_id": store_id,
            "table_id": table_id,
            "role": "table",
        }
    )

    # 4. 활성 세션 확인
    session_id = None
    current_session_id = table.get("current_session_id")
    if current_session_id:
        active_session = session_repository.get_active_session(table_id)
        if active_session:
            session_id = active_session["session_id"]

    return {
        "access_token": token,
        "table_id": table_id,
        "session_id": session_id,
    }
