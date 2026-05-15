"""Category 테이블 데이터 접근 레이어."""

from app.core.dynamodb import get_dynamodb_resource
from app.core.storage import Key


class CategoryRepository:
    """DynamoDB Category 테이블 접근."""

    TABLE_NAME = "Category"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

    def save(self, category: dict) -> dict:
        self._table.put_item(Item=category)
        return category

    def get_by_id(self, store_id: str, category_id: str) -> dict | None:
        response = self._table.get_item(
            Key={"store_id": store_id, "category_id": category_id}
        )
        return response.get("Item")

    def get_by_store(self, store_id: str) -> list[dict]:
        response = self._table.query(
            KeyConditionExpression=Key("store_id").eq(store_id)
        )
        items = response.get("Items", [])
        items.sort(key=lambda x: x.get("sort_order", 0))
        return items

    def update(self, store_id: str, category_id: str, updates: dict) -> dict:
        item = self.get_by_id(store_id, category_id)
        if item:
            item.update(updates)
            self._table.put_item(Item=item)
        return item

    def delete(self, store_id: str, category_id: str) -> None:
        self._table.delete_item(
            Key={"store_id": store_id, "category_id": category_id}
        )
