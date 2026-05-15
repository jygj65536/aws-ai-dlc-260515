"""Order 테이블 데이터 접근 레이어."""

from boto3.dynamodb.conditions import Key

from app.core.dynamodb import get_dynamodb_resource


class OrderRepository:
    """DynamoDB Order 테이블 접근."""

    TABLE_NAME = "Order"

    def __init__(self):
        self._db = get_dynamodb_resource()
        self._table = self._db.Table(self.TABLE_NAME)

    def save(self, order: dict) -> dict:
        """주문 저장."""
        self._table.put_item(Item=order)
        return order

    def get_by_id(self, session_id: str, order_id: str) -> dict | None:
        """주문 단건 조회."""
        response = self._table.get_item(
            Key={"session_id": session_id, "order_id": order_id}
        )
        return response.get("Item")

    def get_by_session(self, session_id: str) -> list[dict]:
        """세션별 주문 목록 조회."""
        response = self._table.query(
            KeyConditionExpression=Key("session_id").eq(session_id)
        )
        return response.get("Items", [])

    def get_by_store(self, store_id: str) -> list[dict]:
        """매장별 주문 목록 조회 (GSI: StoreOrderIndex)."""
        response = self._table.query(
            IndexName="StoreOrderIndex",
            KeyConditionExpression=Key("store_id").eq(store_id),
            ScanIndexForward=False,  # 최신순
        )
        return response.get("Items", [])

    def update_status(self, session_id: str, order_id: str, status: str) -> dict:
        """주문 상태 업데이트."""
        response = self._table.update_item(
            Key={"session_id": session_id, "order_id": order_id},
            UpdateExpression="SET #s = :status",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":status": status},
            ReturnValues="ALL_NEW",
        )
        return response["Attributes"]

    def delete(self, session_id: str, order_id: str) -> None:
        """주문 삭제."""
        self._table.delete_item(
            Key={"session_id": session_id, "order_id": order_id}
        )

    def delete_by_session(self, session_id: str) -> None:
        """세션의 모든 주문 삭제 (이용 완료 시)."""
        orders = self.get_by_session(session_id)
        with self._table.batch_writer() as batch:
            for order in orders:
                batch.delete_item(
                    Key={"session_id": session_id, "order_id": order["order_id"]}
                )

    def get_next_order_number(self, store_id: str) -> int:
        """매장별 다음 주문 번호 조회 (StoreOrderIndex 카운트 + 1)."""
        response = self._table.query(
            IndexName="StoreOrderIndex",
            KeyConditionExpression=Key("store_id").eq(store_id),
            Select="COUNT",
        )
        return response["Count"] + 1
