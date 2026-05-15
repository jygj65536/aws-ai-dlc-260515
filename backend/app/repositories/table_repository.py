"""Table 테이블 데이터 접근 레이어 (주문 기능에서 필요한 부분만)."""

from app.core.dynamodb import get_dynamodb_resource


class TableRepository:
    """DynamoDB Table 테이블 접근."""

    TABLE_NAME = "Table"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

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
