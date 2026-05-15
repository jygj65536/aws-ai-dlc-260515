"""테이블 관리 API 엔드포인트."""

from fastapi import APIRouter, Query

from app.models.table import (
    CompleteTableResponse,
    CreateTableRequest,
    TableHistoryResponse,
    TableResponse,
)
from app.services.table_service import TableService

router = APIRouter()


def _get_service() -> TableService:
    return TableService()


@router.post(
    "/tables",
    response_model=dict,
    status_code=201,
    summary="테이블 생성",
)
async def create_table(request: CreateTableRequest):
    """테이블 생성 (US-7)."""
    service = _get_service()
    return service.create_table(request)


@router.get(
    "/tables",
    response_model=list[TableResponse],
    summary="매장 테이블 목록 조회",
)
async def get_tables(store_id: str = Query(..., description="매장 ID")):
    """매장 테이블 목록 조회 (US-7)."""
    service = _get_service()
    return service.get_tables(store_id)


@router.post(
    "/tables/{table_id}/complete",
    response_model=CompleteTableResponse,
    summary="이용 완료 처리",
)
async def complete_table(
    table_id: str,
    store_id: str = Query(..., description="매장 ID"),
):
    """이용 완료 처리 (US-7).

    - 세션의 모든 주문을 이력으로 이동
    - 테이블 리셋
    - SSE 이벤트 발행
    """
    service = _get_service()
    result = await service.complete_table(store_id, table_id)
    return CompleteTableResponse(**result)


@router.get(
    "/tables/{table_id}/history",
    response_model=list[TableHistoryResponse],
    summary="과거 주문 내역 조회",
)
async def get_table_history(
    table_id: str,
    date_from: str | None = Query(None, description="시작 날짜 (ISO 8601)"),
    date_to: str | None = Query(None, description="종료 날짜 (ISO 8601)"),
):
    """과거 주문 내역 조회 (US-7)."""
    service = _get_service()
    return service.get_table_history(table_id, date_from, date_to)
