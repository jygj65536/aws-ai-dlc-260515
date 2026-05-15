"""Store 테이블 데이터 접근 레이어."""

from app.core.dynamodb import get_dynamodb_resource


class StoreRepository:
    """DynamoDB Store 테이블 접근."""

    TABLE_NAME = "Store"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

    def get_by_id(self, store_id: str) -> dict | None:
        response = self._table.get_item(Key={"store_id": store_id})
        return response.get("Item")
