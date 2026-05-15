"""주문 API 엔드포인트."""

from fastapi import APIRouter, Query

from app.models.order import (
    CreateOrderRequest,
    CreateOrderResponse,
    DeleteOrderResponse,
    OrderResponse,
    UpdateOrderStatusRequest,
    UpdateOrderStatusResponse,
)
from app.services.order_service import OrderService

router = APIRouter()


def _get_order_service() -> OrderService:
    return OrderService()


@router.post(
    "/orders",
    response_model=CreateOrderResponse,
    status_code=201,
    summary="주문 생성",
    description="고객이 장바구니의 메뉴를 주문으로 확정합니다.",
)
async def create_order(request: CreateOrderRequest):
    """주문 생성 (US-3).

    - 세션이 없으면 자동으로 새 세션 생성
    - 주문 번호 자동 부여 (매장별 순번)
    - SSE로 관리자에게 실시간 알림
    """
    service = _get_order_service()
    return await service.create_order(request)


@router.get(
    "/orders",
    response_model=list[OrderResponse],
    summary="주문 목록 조회",
    description="매장별 또는 세션별 주문 목록을 조회합니다.",
)
async def get_orders(
    store_id: str | None = Query(None, description="매장 ID"),
    session_id: str | None = Query(None, description="세션 ID"),
):
    """주문 목록 조회 (US-4, US-6).

    - store_id: 매장의 전체 주문 (관리자용)
    - session_id: 특정 세션의 주문 (고객용)
    """
    service = _get_order_service()
    return await service.get_orders(store_id=store_id, session_id=session_id)


@router.patch(
    "/orders/{order_id}/status",
    response_model=UpdateOrderStatusResponse,
    summary="주문 상태 변경",
    description="관리자가 주문 상태를 변경합니다 (pending → preparing → completed).",
)
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    session_id: str = Query(..., description="주문이 속한 세션 ID"),
):
    """주문 상태 변경 (US-6).

    허용 전이:
    - pending → preparing
    - pending → completed (건너뛰기)
    - preparing → completed
    """
    service = _get_order_service()
    return await service.update_order_status(
        order_id=order_id,
        session_id=session_id,
        new_status=request.status,
    )


@router.delete(
    "/orders/{order_id}",
    response_model=DeleteOrderResponse,
    summary="주문 삭제",
    description="관리자가 주문을 삭제합니다.",
)
async def delete_order(
    order_id: str,
    session_id: str = Query(..., description="주문이 속한 세션 ID"),
):
    """주문 삭제 (US-7).

    - 관리자 전용
    - 세션 총액에서 차감
    - SSE로 실시간 알림
    """
    service = _get_order_service()
    return await service.delete_order(order_id=order_id, session_id=session_id)
