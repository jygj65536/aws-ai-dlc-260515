"""TableSession DynamoDB 리포지토리."""

from datetime import datetime, timezone

from boto3.dynamodb.conditions import Attr, Key

from app.core.dynamodb import dynamodb_resource

TABLE_NAME = "TableSession"


def _get_table():
    return dynamodb_resource.Table(TABLE_NAME)


def get_active_session(table_id: str) -> dict | None:
    """테이블의 활성 세션을 조회한다.

    활성 세션: status="active" AND expires_at > 현재시각

    Args:
        table_id: 테이블 ID (PK)

    Returns:
        활성 세션 dict 또는 None (만료된 경우도 None)
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
    """세션 ID로 세션을 조회한다.

    Args:
        table_id: 테이블 ID (PK)
        session_id: 세션 ID (SK)

    Returns:
        세션 dict 또는 None
    """
    table = _get_table()
    response = table.get_item(Key={"table_id": table_id, "session_id": session_id})
    return response.get("Item")
