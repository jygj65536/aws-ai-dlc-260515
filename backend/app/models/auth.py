"""인증 관련 요청/응답 스키마."""

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    """관리자 로그인 요청."""

    store_id: str = Field(..., description="매장 ID")
    username: str = Field(..., description="사용자명")
    password: str = Field(..., description="비밀번호")


class TableLoginRequest(BaseModel):
    """테이블 태블릿 로그인 요청."""

    store_id: str = Field(..., description="매장 ID")
    table_number: int = Field(..., description="테이블 번호")
    password: str = Field(..., description="테이블 비밀번호")


class TokenResponse(BaseModel):
    """토큰 응답 (관리자 로그인)."""

    access_token: str = Field(..., description="JWT 액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")


class TableTokenResponse(BaseModel):
    """토큰 응답 (테이블 로그인)."""

    access_token: str = Field(..., description="JWT 액세스 토큰")
    table_id: str = Field(..., description="테이블 ID")
    session_id: str | None = Field(None, description="현재 활성 세션 ID (없으면 null)")


class CurrentUserResponse(BaseModel):
    """현재 인증 정보 응답."""

    user_type: str = Field(..., description="사용자 유형 (admin/table)")
    store_id: str = Field(..., description="매장 ID")
    user_id: str | None = Field(None, description="관리자 username (admin인 경우)")
    table_id: str | None = Field(None, description="테이블 ID (table인 경우)")


class ErrorResponse(BaseModel):
    """에러 응답."""

    detail: str = Field(..., description="에러 메시지 (한국어)")
