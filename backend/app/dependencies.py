"""의존성 주입 모듈.

인증 관련 의존성은 feature/auth 브랜치에서 실제 구현 예정.
현재는 개발/테스트용 스텁으로 제공.
"""

from dataclasses import dataclass

from fastapi import Header, HTTPException, status

from app.services.order_service import OrderService
from app.services.sse_manager import sse_manager, SSEManager


@dataclass
class CurrentUser:
    """인증된 사용자 컨텍스트."""

    store_id: str
    user_id: str  # admin username 또는 table_id
    role: str  # "admin" 또는 "table"


async def get_current_user(
    authorization: str | None = Header(None),
) -> CurrentUser:
    """현재 인증된 사용자 반환 (스텁).

    TODO: feature/auth 브랜치에서 실제 JWT 검증으로 교체
    현재는 개발 편의를 위해 헤더 없이도 기본 사용자 반환.
    """
    if authorization and authorization.startswith("Bearer "):
        # 실제 JWT 검증은 feature/auth에서 구현
        # 현재는 토큰이 있으면 기본 admin으로 처리
        return CurrentUser(
            store_id="dev-store",
            user_id="dev-admin",
            role="admin",
        )

    # 개발 모드: 인증 없이 기본 사용자 반환
    return CurrentUser(
        store_id="dev-store",
        user_id="dev-user",
        role="admin",
    )


async def require_admin(
    authorization: str | None = Header(None),
) -> CurrentUser:
    """관리자 권한 필수 (스텁).

    TODO: feature/auth 브랜치에서 실제 구현
    """
    user = await get_current_user(authorization)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다",
        )
    return user


async def require_table(
    authorization: str | None = Header(None),
) -> CurrentUser:
    """테이블 권한 필수 (스텁).

    TODO: feature/auth 브랜치에서 실제 구현
    """
    user = await get_current_user(authorization)
    # 개발 모드에서는 모든 역할 허용
    return user


def get_order_service() -> OrderService:
    """OrderService 인스턴스 반환."""
    return OrderService()


def get_sse_manager() -> SSEManager:
    """SSEManager 싱글톤 반환."""
    return sse_manager
