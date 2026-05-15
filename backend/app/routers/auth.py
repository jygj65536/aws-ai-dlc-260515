"""인증 API 라우터."""

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.auth import (
    AdminLoginRequest,
    CurrentUserResponse,
    TableLoginRequest,
    TableTokenResponse,
    TokenResponse,
)
from app.services import auth_service

router = APIRouter()


@router.post(
    "/admin/login",
    response_model=TokenResponse,
    summary="관리자 로그인",
    responses={
        401: {"description": "잘못된 자격증명"},
        423: {"description": "계정 잠금"},
    },
)
async def admin_login(request: AdminLoginRequest):
    """관리자 로그인 API.

    - 매장 ID, 사용자명, 비밀번호로 인증
    - 성공 시 JWT 토큰 반환 (16시간 유효)
    - 5회 연속 실패 시 15분 계정 잠금
    """
    result = auth_service.admin_login(
        store_id=request.store_id,
        username=request.username,
        password=request.password,
    )
    return TokenResponse(**result)


@router.post(
    "/table/login",
    response_model=TableTokenResponse,
    summary="테이블 태블릿 로그인",
    responses={
        401: {"description": "잘못된 자격증명"},
    },
)
async def table_login(request: TableLoginRequest):
    """테이블 태블릿 로그인 API.

    - 매장 ID, 테이블 번호, 비밀번호로 인증
    - 성공 시 JWT 토큰 + 테이블 ID + 활성 세션 ID 반환
    - 활성 세션이 없으면 session_id는 null (첫 주문 시 자동 생성)
    """
    result = auth_service.table_login(
        store_id=request.store_id,
        table_number=request.table_number,
        password=request.password,
    )
    return TableTokenResponse(**result)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="현재 인증 정보 확인",
    responses={
        401: {"description": "인증 필요"},
    },
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """현재 인증된 사용자 정보를 반환한다.

    - Bearer 토큰 필요
    - 토큰에서 추출한 사용자 유형, 매장 ID, 식별자 반환
    """
    role = current_user.get("role")
    return CurrentUserResponse(
        user_type=role,
        store_id=current_user.get("store_id"),
        user_id=current_user.get("username") if role == "admin" else None,
        table_id=current_user.get("table_id") if role == "table" else None,
    )
