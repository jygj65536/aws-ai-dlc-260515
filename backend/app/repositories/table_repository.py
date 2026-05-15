"""Table DynamoDB 리포지토리."""

from boto3.dynamodb.conditions import Key

from app.core.dynamodb import dynamodb_resource

TABLE_NAME = "Table"


def _get_table():
    return dynamodb_resource.Table(TABLE_NAME)


def get_by_table_number(store_id: str, table_number: int) -> dict | None:
    """store_id와 table_number로 테이블 조회 (GSI: TableNumberIndex).

    Args:
        store_id: 매장 ID
        table_number: 테이블 번호

    Returns:
        테이블 정보 dict 또는 None
    """
    table = _get_table()
    response = table.query(
        IndexName="TableNumberIndex",
        KeyConditionExpression=Key("store_id").eq(store_id)
        & Key("table_number").eq(table_number),
    )
    items = response.get("Items", [])
    return items[0] if items else None


def get_by_id(store_id: str, table_id: str) -> dict | None:
    """store_id와 table_id로 테이블 조회.

    Args:
        store_id: 매장 ID (PK)
        table_id: 테이블 ID (SK)

    Returns:
        테이블 정보 dict 또는 None
    """
    table = _get_table()
    response = table.get_item(Key={"store_id": store_id, "table_id": table_id})
    return response.get("Item")
