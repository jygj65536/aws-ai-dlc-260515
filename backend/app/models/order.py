"""주문 관련 Pydantic 스키마."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """주문 상태."""

    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


# --- 요청 스키마 ---


class OrderItemRequest(BaseModel):
    """주문 항목 요청."""

    menu_id: str = Field(..., description="메뉴 ID")
    name: str = Field(..., description="메뉴명")
    quantity: int = Field(..., ge=1, le=99, description="수량 (1~99)")
    price: int = Field(..., gt=0, description="단가 (원)")


class CreateOrderRequest(BaseModel):
    """주문 생성 요청."""

    store_id: str = Field(..., description="매장 ID")
    table_id: str = Field(..., description="테이블 ID")
    session_id: str | None = Field(None, description="세션 ID (null이면 새 세션 생성)")
    items: list[OrderItemRequest] = Field(
        ..., min_length=1, description="주문 항목 (1개 이상)"
    )


class UpdateOrderStatusRequest(BaseModel):
    """주문 상태 변경 요청."""

    status: OrderStatus = Field(..., description="변경할 상태")


# --- 응답 스키마 ---


class OrderItemResponse(BaseModel):
    """주문 항목 응답."""

    menu_id: str
    name: str
    quantity: int
    price: int
    subtotal: int


class CreateOrderResponse(BaseModel):
    """주문 생성 응답."""

    order_id: str
    order_number: int
    total_amount: int
    session_id: str


class OrderResponse(BaseModel):
    """주문 상세 응답."""

    order_id: str
    session_id: str
    store_id: str
    table_id: str
    order_number: int
    status: OrderStatus
    items: list[OrderItemResponse]
    total_amount: int
    created_at: str


class UpdateOrderStatusResponse(BaseModel):
    """주문 상태 변경 응답."""

    order_id: str
    status: OrderStatus


class DeleteOrderResponse(BaseModel):
    """주문 삭제 응답."""

    success: bool = True


class OrderHistoryResponse(BaseModel):
    """과거 주문 이력 응답."""

    history_id: str
    session_id: str
    orders: list[OrderResponse]
    total_amount: int
    completed_at: str
