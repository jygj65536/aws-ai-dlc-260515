"""Table 테이블 데이터 접근 레이어."""

from app.core.storage import Key

from app.core.dynamodb import get_dynamodb_resource

TABLE_NAME = "Table"


def _get_table():
    return get_dynamodb_resource().Table(TABLE_NAME)


# --- 모듈 레벨 함수 (auth_service에서 사용) ---


def get_by_table_number(store_id: str, table_number: int) -> dict | None:
    """store_id와 table_number로 테이블 조회 (GSI: TableNumberIndex)."""
    table = _get_table()
    response = table.query(
        IndexName="TableNumberIndex",
        KeyConditionExpression=Key("store_id").eq(store_id)
        & Key("table_number").eq(table_number),
    )
    items = response.get("Items", [])
    return items[0] if items else None


def get_by_id(store_id: str, table_id: str) -> dict | None:
    """store_id와 table_id로 테이블 조회."""
    table = _get_table()
    response = table.get_item(Key={"store_id": store_id, "table_id": table_id})
    return response.get("Item")


# --- 클래스 기반 (order_service에서 사용) ---


class TableRepository:
    """DynamoDB Table 테이블 접근."""

    def __init__(self):
        self._table = _get_table()

    def get_by_id(self, store_id: str, table_id: str) -> dict | None:
        """테이블 단건 조회."""
        response = self._table.get_item(
            Key={"store_id": store_id, "table_id": table_id}
        )
        return response.get("Item")

    def update_session_id(
        self, store_id: str, table_id: str, session_id: str | None
    ) -> None:
        """테이블의 현재 세션 ID 업데이트."""
        if session_id is None:
            self._table.update_item(
                Key={"store_id": store_id, "table_id": table_id},
                UpdateExpression="REMOVE current_session_id",
            )
        else:
            self._table.update_item(
                Key={"store_id": store_id, "table_id": table_id},
                UpdateExpression="SET current_session_id = :sid",
                ExpressionAttributeValues={":sid": session_id},
            )
