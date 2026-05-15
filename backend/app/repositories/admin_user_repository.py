"""AdminUser DynamoDB 리포지토리."""

from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key

from app.core.dynamodb import get_dynamodb_resource

TABLE_NAME = "AdminUser"


def _get_table():
    return get_dynamodb_resource().Table(TABLE_NAME)


def get_by_username(store_id: str, username: str) -> dict | None:
    """store_id와 username으로 관리자 조회.

    Args:
        store_id: 매장 ID (PK)
        username: 사용자명 (SK)

    Returns:
        관리자 정보 dict 또는 None
    """
    table = _get_table()
    response = table.get_item(Key={"store_id": store_id, "username": username})
    return response.get("Item")


def update_login_attempts(store_id: str, username: str, attempts: int) -> None:
    """로그인 시도 횟수를 업데이트한다.

    Args:
        store_id: 매장 ID
        username: 사용자명
        attempts: 새 시도 횟수
    """
    table = _get_table()
    table.update_item(
        Key={"store_id": store_id, "username": username},
        UpdateExpression="SET login_attempts = :attempts",
        ExpressionAttributeValues={":attempts": attempts},
    )


def lock_account(store_id: str, username: str, locked_until: str) -> None:
    """계정을 잠금 처리한다.

    Args:
        store_id: 매장 ID
        username: 사용자명
        locked_until: 잠금 해제 시각 (ISO 8601)
    """
    table = _get_table()
    table.update_item(
        Key={"store_id": store_id, "username": username},
        UpdateExpression="SET locked_until = :locked_until, login_attempts = :attempts",
        ExpressionAttributeValues={
            ":locked_until": locked_until,
            ":attempts": 5,
        },
    )


def reset_login_attempts(store_id: str, username: str) -> None:
    """로그인 성공 시 시도 횟수와 잠금을 초기화한다.

    Args:
        store_id: 매장 ID
        username: 사용자명
    """
    table = _get_table()
    table.update_item(
        Key={"store_id": store_id, "username": username},
        UpdateExpression="SET login_attempts = :zero REMOVE locked_until",
        ExpressionAttributeValues={":zero": 0},
    )
