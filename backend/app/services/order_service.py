"""주문 비즈니스 로직 서비스."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException, status

from app.config import get_settings
from app.models.order import (
    CreateOrderRequest,
    CreateOrderResponse,
    DeleteOrderResponse,
    OrderResponse,
    OrderStatus,
    UpdateOrderStatusResponse,
)
from app.repositories.order_repository import OrderRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.table_repository import TableRepository
from app.services.sse_manager import sse_manager


# 허용되는 상태 전이 맵
VALID_TRANSITIONS: dict[str, set[str]] = {
    OrderStatus.PENDING: {OrderStatus.PREPARING, OrderStatus.COMPLETED},
    OrderStatus.PREPARING: {OrderStatus.COMPLETED},
    OrderStatus.COMPLETED: set(),  # 완료 후 변경 불가
}


class OrderService:
    """주문 비즈니스 로직."""

    def __init__(self):
        self._order_repo = OrderRepository()
        self._session_repo = SessionRepository()
        self._table_repo = TableRepository()

    async def create_order(self, request: CreateOrderRequest) -> CreateOrderResponse:
        """주문 생성.

        - 세션이 없으면 새 세션 생성
        - 세션이 만료되었으면 새 세션 생성
        - 주문 번호 자동 생성 (매장별 순번)
        - SSE 이벤트 발행
        """
        # 세션 처리
        session_id = await self._ensure_active_session(
            store_id=request.store_id,
            table_id=request.table_id,
            session_id=request.session_id,
        )

        # 주문 번호 생성
        order_number = self._order_repo.get_next_order_number(request.store_id)

        # 총액 계산
        items_with_subtotal = []
        total_amount = 0
        for item in request.items:
            subtotal = item.quantity * item.price
            total_amount += subtotal
            items_with_subtotal.append(
                {
                    "menu_id": item.menu_id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "subtotal": subtotal,
                }
            )

        # 주문 저장
        order_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        order_data = {
            "session_id": session_id,
            "order_id": order_id,
            "store_id": request.store_id,
            "table_id": request.table_id,
            "order_number": order_number,
            "status": OrderStatus.PENDING,
            "items": items_with_subtotal,
            "total_amount": total_amount,
            "created_at": now,
        }

        self._order_repo.save(order_data)

        # 세션 총액 업데이트
        self._session_repo.update_total_amount(
            table_id=request.table_id,
            session_id=session_id,
            amount_delta=total_amount,
        )

        # SSE 이벤트 발행
        await sse_manager.broadcast(
            store_id=request.store_id,
            event_type="new_order",
            data={
                "order_id": order_id,
                "order_number": order_number,
                "table_id": request.table_id,
                "items": items_with_subtotal,
                "total_amount": total_amount,
                "status": OrderStatus.PENDING,
                "created_at": now,
            },
        )

        return CreateOrderResponse(
            order_id=order_id,
            order_number=order_number,
            total_amount=total_amount,
            session_id=session_id,
        )

    async def get_orders(
        self,
        store_id: str | None = None,
        session_id: str | None = None,
    ) -> list[OrderResponse]:
        """주문 목록 조회."""
        if session_id:
            orders = self._order_repo.get_by_session(session_id)
        elif store_id:
            orders = self._order_repo.get_by_store(store_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="store_id 또는 session_id가 필요합니다",
            )

        return [self._to_order_response(order) for order in orders]

    async def update_order_status(
        self,
        order_id: str,
        session_id: str,
        new_status: OrderStatus,
    ) -> UpdateOrderStatusResponse:
        """주문 상태 변경.

        상태 전이 규칙:
        - pending → preparing ✅
        - pending → completed ✅ (건너뛰기 허용)
        - preparing → completed ✅
        - completed → * ❌
        - preparing → pending ❌
        """
        order = self._order_repo.get_by_id(session_id, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="주문을 찾을 수 없습니다",
            )

        current_status = order["status"]
        self._validate_status_transition(current_status, new_status)

        self._order_repo.update_status(session_id, order_id, new_status)

        # SSE 이벤트 발행
        await sse_manager.broadcast(
            store_id=order["store_id"],
            event_type="order_updated",
            data={"order_id": order_id, "status": new_status},
        )

        return UpdateOrderStatusResponse(order_id=order_id, status=new_status)

    async def delete_order(
        self, order_id: str, session_id: str
    ) -> DeleteOrderResponse:
        """주문 삭제 (관리자 전용)."""
        order = self._order_repo.get_by_id(session_id, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="주문을 찾을 수 없습니다",
            )

        # 주문 삭제
        self._order_repo.delete(session_id, order_id)

        # 세션 총액 차감
        total_amount = int(order.get("total_amount", 0))
        self._session_repo.update_total_amount(
            table_id=order["table_id"],
            session_id=session_id,
            amount_delta=-total_amount,
        )

        # SSE 이벤트 발행
        await sse_manager.broadcast(
            store_id=order["store_id"],
            event_type="order_deleted",
            data={"order_id": order_id, "table_id": order["table_id"]},
        )

        return DeleteOrderResponse(success=True)

    async def _ensure_active_session(
        self, store_id: str, table_id: str, session_id: str | None
    ) -> str:
        """활성 세션 확인 및 생성.

        - session_id가 None이면 새 세션 생성
        - session_id가 있으면 유효성 확인 (만료 시 새 세션 생성)
        """
        settings = get_settings()
        now = datetime.now(timezone.utc)

        if session_id:
            # 기존 세션 확인
            session = self._session_repo.get_by_id(table_id, session_id)
            if session:
                expires_at = datetime.fromisoformat(session["expires_at"])
                if session["status"] == "active" and expires_at > now:
                    return session_id
                # 만료된 세션 처리 (Lazy Expiration)
                if session["status"] == "active" and expires_at <= now:
                    self._session_repo.update_status(
                        table_id, session_id, "expired"
                    )

        # 새 세션 생성
        new_session_id = str(uuid.uuid4())
        expires_at = now + timedelta(hours=settings.session_expire_hours)

        session_data = {
            "table_id": table_id,
            "session_id": new_session_id,
            "store_id": store_id,
            "status": "active",
            "started_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "completed_at": None,
            "total_amount": Decimal("0"),
        }

        self._session_repo.create(session_data)

        # 테이블의 현재 세션 업데이트
        self._table_repo.update_session_id(store_id, table_id, new_session_id)

        return new_session_id

    def _validate_status_transition(
        self, current: str, new: OrderStatus
    ) -> None:
        """상태 전이 유효성 검증."""
        valid_next = VALID_TRANSITIONS.get(current, set())
        if new not in valid_next:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"상태 전이 불가: {current} → {new}",
            )

    def _to_order_response(self, order: dict) -> OrderResponse:
        """DynamoDB 아이템을 OrderResponse로 변환."""
        items = order.get("items", [])
        # Decimal → int 변환
        converted_items = []
        for item in items:
            converted_items.append(
                {
                    "menu_id": item["menu_id"],
                    "name": item["name"],
                    "quantity": int(item["quantity"]),
                    "price": int(item["price"]),
                    "subtotal": int(item["subtotal"]),
                }
            )

        return OrderResponse(
            order_id=order["order_id"],
            session_id=order["session_id"],
            store_id=order["store_id"],
            table_id=order["table_id"],
            order_number=int(order["order_number"]),
            status=order["status"],
            items=converted_items,
            total_amount=int(order["total_amount"]),
            created_at=order["created_at"],
        )
