"""OrderHistory 테이블 데이터 접근 레이어."""

from boto3.dynamodb.conditions import Key

from app.core.dynamodb import get_dynamodb_resource


class OrderHistoryRepository:
    """DynamoDB OrderHistory 테이블 접근."""

    TABLE_NAME = "OrderHistory"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

    def save(self, history: dict) -> dict:
        """이력 저장."""
        self._table.put_item(Item=history)
        return history

    def get_by_table(
        self, table_id: str, date_from: str | None = None, date_to: str | None = None
    ) -> list[dict]:
        """테이블별 이력 조회 (날짜 필터 옵션)."""
        if date_from and date_to:
            response = self._table.query(
                IndexName="DateIndex",
                KeyConditionExpression=(
                    Key("table_id").eq(table_id)
                    & Key("completed_at").between(date_from, date_to)
                ),
                ScanIndexForward=False,
            )
        elif date_from:
            response = self._table.query(
                IndexName="DateIndex",
                KeyConditionExpression=(
                    Key("table_id").eq(table_id)
                    & Key("completed_at").gte(date_from)
                ),
                ScanIndexForward=False,
            )
        elif date_to:
            response = self._table.query(
                IndexName="DateIndex",
                KeyConditionExpression=(
                    Key("table_id").eq(table_id)
                    & Key("completed_at").lte(date_to)
                ),
                ScanIndexForward=False,
            )
        else:
            response = self._table.query(
                KeyConditionExpression=Key("table_id").eq(table_id),
                ScanIndexForward=False,
            )
        return response.get("Items", [])
