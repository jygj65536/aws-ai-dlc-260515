"""테이블 관리 비즈니스 로직 서비스."""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.table import CreateTableRequest
from app.repositories.order_history_repository import OrderHistoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.table_repository import TableRepository
from app.services.sse_manager import sse_manager
from app.core.storage import Key, get_table

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TableService:
    """테이블 관리 비즈니스 로직."""

    def __init__(self):
        self._table_repo = TableRepository()
        self._session_repo = SessionRepository()
        self._order_repo = OrderRepository()
        self._history_repo = OrderHistoryRepository()

    def create_table(self, request: CreateTableRequest) -> dict:
        """테이블 생성."""
        # 중복 확인
        from app.repositories.table_repository import get_by_table_number
        existing = get_by_table_number(request.store_id, request.table_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 테이블 번호입니다",
            )

        table_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        table_data = {
            "store_id": request.store_id,
            "table_id": table_id,
            "table_number": request.table_number,
            "password_hash": pwd_context.hash(request.password),
            "current_session_id": None,
            "created_at": now,
        }

        db_table = get_table("Table")
        db_table.put_item(Item=table_data)

        return {"table_id": table_id, "table_number": request.table_number}

    def get_tables(self, store_id: str) -> list[dict]:
        """매장 테이블 목록 조회."""
        db_table = get_table("Table")
        response = db_table.query(
            KeyConditionExpression=Key("store_id").eq(store_id)
        )
        items = response.get("Items", [])
        result = []
        for item in items:
            result.append({
                "table_id": item["table_id"],
                "store_id": item["store_id"],
                "table_number": int(item["table_number"]),
                "current_session_id": item.get("current_session_id"),
            })
        result.sort(key=lambda x: x["table_number"])
        return result

    async def complete_table(self, store_id: str, table_id: str) -> dict:
        """이용 완료 처리.

        1. 테이블 조회 → 현재 세션 확인
        2. 세션의 모든 주문 조회
        3. OrderHistory 생성
        4. 주문 삭제
        5. 세션 완료 처리
        6. 테이블 리셋
        7. SSE 이벤트 발행
        """
        table = self._table_repo.get_by_id(store_id, table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="테이블을 찾을 수 없습니다",
            )

        session_id = table.get("current_session_id")
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="활성 세션이 없습니다",
            )

        # 세션의 모든 주문 조회
        orders = self._order_repo.get_by_session(session_id)

        # 총액 계산
        total_amount = sum(int(o.get("total_amount", 0)) for o in orders)

        # OrderHistory 생성
        now = datetime.now(timezone.utc).isoformat()
        history_id = str(uuid.uuid4())
        history_data = {
            "table_id": table_id,
            "history_id": history_id,
            "store_id": store_id,
            "session_id": session_id,
            "orders": orders,
            "total_amount": total_amount,
            "completed_at": now,
        }
        self._history_repo.save(history_data)

        # 주문 삭제
        self._order_repo.delete_by_session(session_id)

        # 세션 완료 처리
        self._session_repo.update_status(table_id, session_id, "completed", now)

        # 테이블 리셋
        self._table_repo.update_session_id(store_id, table_id, None)

        # SSE 이벤트 발행
        await sse_manager.broadcast(
            store_id=store_id,
            event_type="table_completed",
            data={"table_id": table_id},
        )

        return {"success": True, "message": "이용 완료 처리됨"}

    def get_table_history(
        self, table_id: str, date_from: str | None = None, date_to: str | None = None
    ) -> list[dict]:
        """과거 주문 내역 조회."""
        histories = self._history_repo.get_by_table(table_id, date_from, date_to)
        result = []
        for h in histories:
            result.append({
                "history_id": h["history_id"],
                "session_id": h["session_id"],
                "orders": h.get("orders", []),
                "total_amount": int(h.get("total_amount", 0)),
                "completed_at": h["completed_at"],
            })
        return result
