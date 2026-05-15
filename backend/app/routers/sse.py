"""SSE (Server-Sent Events) 스트림 엔드포인트."""

import asyncio
import json

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.services.sse_manager import sse_manager

router = APIRouter()


@router.get(
    "/sse/orders/{store_id}",
    summary="주문 실시간 스트림",
    description="매장의 주문 이벤트를 실시간으로 수신합니다 (SSE).",
)
async def order_stream(store_id: str):
    """주문 실시간 SSE 스트림 (US-6).

    이벤트 타입:
    - new_order: 새 주문 생성
    - order_updated: 주문 상태 변경
    - order_deleted: 주문 삭제
    - table_completed: 테이블 이용 완료
    """

    async def event_generator():
        queue = sse_manager.connect(store_id)
        try:
            while True:
                try:
                    # 30초 타임아웃으로 keep-alive ping 전송
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield {
                        "event": event["event"],
                        "data": event["data"],
                    }
                except asyncio.TimeoutError:
                    # keep-alive ping
                    yield {"event": "ping", "data": json.dumps({"type": "ping"})}
        except asyncio.CancelledError:
            pass
        finally:
            sse_manager.disconnect(store_id, queue)

    return EventSourceResponse(event_generator())
