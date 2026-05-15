"""TableSession 테이블 데이터 접근 레이어."""

from datetime import datetime, timezone
from decimal import Decimal

from app.core.storage import Attr, Key

from app.core.dynamodb import get_dynamodb_resource

TABLE_NAME = "TableSession"


def _get_table():
    return get_dynamodb_resource().Table(TABLE_NAME)


# --- 모듈 레벨 함수 (auth_service에서 사용) ---


def get_active_session(table_id: str) -> dict | None:
    """테이블의 활성 세션을 조회한다.

    활성 세션: status="active" AND expires_at > 현재시각
    """
    table = _get_table()
    now = datetime.now(timezone.utc).isoformat()

    response = table.query(
        KeyConditionExpression=Key("table_id").eq(table_id),
        FilterExpression=Attr("status").eq("active") & Attr("expires_at").gt(now),
        ScanIndexForward=False,
        Limit=1,
    )
    items = response.get("Items", [])
    return items[0] if items else None


def get_session_by_id(table_id: str, session_id: str) -> dict | None:
    """세션 ID로 세션을 조회한다."""
    table = _get_table()
    response = table.get_item(Key={"table_id": table_id, "session_id": session_id})
    return response.get("Item")


# --- 클래스 기반 (order_service에서 사용) ---


class SessionRepository:
    """DynamoDB TableSession 테이블 접근."""

    def __init__(self):
        self._table = _get_table()

    def create(self, session: dict) -> dict:
        """세션 생성."""
        self._table.put_item(Item=session)
        return session

    def get_by_id(self, table_id: str, session_id: str) -> dict | None:
        """세션 단건 조회."""
        response = self._table.get_item(
            Key={"table_id": table_id, "session_id": session_id}
        )
        return response.get("Item")

    def get_active_by_table(self, table_id: str) -> dict | None:
        """테이블의 활성 세션 조회."""
        response = self._table.query(
            KeyConditionExpression=Key("table_id").eq(table_id),
            ScanIndexForward=False,
            Limit=10,
        )
        items = response.get("Items", [])
        for item in items:
            if item.get("status") == "active":
                return item
        return None

    def update_total_amount(
        self, table_id: str, session_id: str, amount_delta: int
    ) -> None:
        """세션 총액 업데이트 (증감)."""
        self._table.update_item(
            Key={"table_id": table_id, "session_id": session_id},
            UpdateExpression="SET total_amount = total_amount + :delta",
            ExpressionAttributeValues={":delta": Decimal(str(amount_delta))},
        )

    def update_status(
        self, table_id: str, session_id: str, status: str, completed_at: str | None = None
    ) -> None:
        """세션 상태 업데이트."""
        if completed_at:
            self._table.update_item(
                Key={"table_id": table_id, "session_id": session_id},
                UpdateExpression="SET #s = :status, completed_at = :completed_at",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={
                    ":status": status,
                    ":completed_at": completed_at,
                },
            )
        else:
            self._table.update_item(
                Key={"table_id": table_id, "session_id": session_id},
                UpdateExpression="SET #s = :status",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":status": status},
            )
