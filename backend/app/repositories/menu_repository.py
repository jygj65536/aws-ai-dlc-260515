"""MenuItem 테이블 데이터 접근 레이어."""

from app.core.dynamodb import get_dynamodb_resource
from app.core.storage import Key


class MenuRepository:
    """DynamoDB MenuItem 테이블 접근."""

    TABLE_NAME = "MenuItem"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

    def save(self, menu: dict) -> dict:
        self._table.put_item(Item=menu)
        return menu

    def get_by_id(self, store_id: str, menu_id: str) -> dict | None:
        response = self._table.get_item(
            Key={"store_id": store_id, "menu_id": menu_id}
        )
        return response.get("Item")

    def get_by_store(self, store_id: str, available_only: bool = False) -> list[dict]:
        response = self._table.query(
            KeyConditionExpression=Key("store_id").eq(store_id)
        )
        items = response.get("Items", [])
        if available_only:
            items = [i for i in items if i.get("is_available", True)]
        items.sort(key=lambda x: x.get("sort_order", 0))
        return items

    def update(self, store_id: str, menu_id: str, updates: dict) -> dict:
        item = self.get_by_id(store_id, menu_id)
        if item:
            item.update(updates)
            self._table.put_item(Item=item)
        return item

    def delete(self, store_id: str, menu_id: str) -> None:
        self._table.delete_item(
            Key={"store_id": store_id, "menu_id": menu_id}
        )
