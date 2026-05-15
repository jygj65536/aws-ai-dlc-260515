"""SSE (Server-Sent Events) 연결 관리 모듈."""

import asyncio
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class SSEManager:
    """매장별 SSE 연결 관리 및 이벤트 브로드캐스트."""

    def __init__(self):
        # store_id → set of asyncio.Queue
        self._connections: dict[str, set[asyncio.Queue]] = {}

    def connect(self, store_id: str) -> asyncio.Queue:
        """새 SSE 연결 등록. 이벤트를 수신할 Queue 반환."""
        if store_id not in self._connections:
            self._connections[store_id] = set()
        queue: asyncio.Queue = asyncio.Queue()
        self._connections[store_id].add(queue)
        logger.info(
            "SSE 연결 등록: store_id=%s, 총 연결 수=%d",
            store_id,
            len(self._connections[store_id]),
        )
        return queue

    def disconnect(self, store_id: str, queue: asyncio.Queue) -> None:
        """SSE 연결 해제."""
        if store_id in self._connections:
            self._connections[store_id].discard(queue)
            if not self._connections[store_id]:
                del self._connections[store_id]
            logger.info("SSE 연결 해제: store_id=%s", store_id)

    async def broadcast(
        self, store_id: str, event_type: str, data: Any
    ) -> None:
        """매장의 모든 활성 연결에 이벤트 브로드캐스트."""
        if store_id not in self._connections:
            return

        event = {
            "event": event_type,
            "data": json.dumps(data, ensure_ascii=False, default=str),
        }

        dead_connections: list[asyncio.Queue] = []
        for queue in self._connections[store_id]:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                dead_connections.append(queue)
                logger.warning("SSE 큐 가득 참, 연결 제거: store_id=%s", store_id)

        # 실패한 연결 제거
        for queue in dead_connections:
            self._connections[store_id].discard(queue)

    def get_connection_count(self, store_id: str) -> int:
        """매장의 활성 연결 수 반환."""
        return len(self._connections.get(store_id, set()))


# 싱글톤 인스턴스
sse_manager = SSEManager()
