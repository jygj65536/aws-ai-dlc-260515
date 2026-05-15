"""FastAPI 의존성 주입 모듈 (인증/인가 + 서비스)."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.services.order_service import OrderService
from app.services.sse_manager import sse_manager, SSEManager

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> dict:
    """JWT 토큰을 검증하고 현재 사용자 컨텍스트를 반환한다.

    Returns:
        {"store_id": str, "role": str, "username"?: str, "table_id"?: str}

    Raises:
        HTTPException: 401 (토큰 없음/만료/유효하지 않음)
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다",
        )
    return payload


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """관리자 권한을 요구한다.

    비즈니스 규칙 AUTH-04: role != "admin" → 403

    Returns:
        관리자 사용자 컨텍스트

    Raises:
        HTTPException: 403 (권한 없음)
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다",
        )
    return current_user


async def require_table(current_user: dict = Depends(get_current_user)) -> dict:
    """테이블 권한을 요구한다.

    비즈니스 규칙 AUTH-05: role != "table" → 403

    Returns:
        테이블 사용자 컨텍스트

    Raises:
        HTTPException: 403 (권한 없음)
    """
    if current_user.get("role") != "table":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="테이블 권한이 필요합니다",
        )
    return current_user


def require_store_match(store_id: str, current_user: dict) -> None:
    """요청의 store_id와 토큰의 store_id 일치를 검증한다.

    비즈니스 규칙 AUTH-06: 매장 격리

    Args:
        store_id: 요청에 포함된 매장 ID
        current_user: 토큰에서 추출한 사용자 컨텍스트

    Raises:
        HTTPException: 403 (매장 불일치)
    """
    if current_user.get("store_id") != store_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 매장에 대한 접근 권한이 없습니다",
        )


def get_order_service() -> OrderService:
    """OrderService 인스턴스 반환."""
    return OrderService()


def get_sse_manager() -> SSEManager:
    """SSEManager 싱글톤 반환."""
    return sse_manager
