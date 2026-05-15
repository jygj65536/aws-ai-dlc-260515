"""로컬 DynamoDB 테이블 생성 스크립트.

사용법:
    python -m scripts.create_tables

사전 조건:
    - 로컬 DynamoDB가 실행 중이어야 합니다.
    - docker run -p 8000:8000 amazon/dynamodb-local
"""

import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.dynamodb import get_dynamodb_client


def create_store_table(client):
    """Store 테이블 생성."""
    try:
        client.create_table(
            TableName="Store",
            KeySchema=[{"AttributeName": "store_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "store_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print("✅ Store 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  Store 테이블 이미 존재")


def create_admin_user_table(client):
    """AdminUser 테이블 생성."""
    try:
        client.create_table(
            TableName="AdminUser",
            KeySchema=[
                {"AttributeName": "store_id", "KeyType": "HASH"},
                {"AttributeName": "username", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "store_id", "AttributeType": "S"},
                {"AttributeName": "username", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print("✅ AdminUser 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  AdminUser 테이블 이미 존재")


def create_table_table(client):
    """Table 테이블 생성."""
    try:
        client.create_table(
            TableName="Table",
            KeySchema=[
                {"AttributeName": "store_id", "KeyType": "HASH"},
                {"AttributeName": "table_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "store_id", "AttributeType": "S"},
                {"AttributeName": "table_id", "AttributeType": "S"},
                {"AttributeName": "table_number", "AttributeType": "N"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "TableNumberIndex",
                    "KeySchema": [
                        {"AttributeName": "store_id", "KeyType": "HASH"},
                        {"AttributeName": "table_number", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("✅ Table 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  Table 테이블 이미 존재")


def create_table_session_table(client):
    """TableSession 테이블 생성."""
    try:
        client.create_table(
            TableName="TableSession",
            KeySchema=[
                {"AttributeName": "table_id", "KeyType": "HASH"},
                {"AttributeName": "session_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "table_id", "AttributeType": "S"},
                {"AttributeName": "session_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("✅ TableSession 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  TableSession 테이블 이미 존재")


def create_order_table(client):
    """Order 테이블 생성."""
    try:
        client.create_table(
            TableName="Order",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "order_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "order_id", "AttributeType": "S"},
                {"AttributeName": "store_id", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "StoreOrderIndex",
                    "KeySchema": [
                        {"AttributeName": "store_id", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("✅ Order 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  Order 테이블 이미 존재")


def create_order_history_table(client):
    """OrderHistory 테이블 생성."""
    try:
        client.create_table(
            TableName="OrderHistory",
            KeySchema=[
                {"AttributeName": "table_id", "KeyType": "HASH"},
                {"AttributeName": "history_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "table_id", "AttributeType": "S"},
                {"AttributeName": "history_id", "AttributeType": "S"},
                {"AttributeName": "completed_at", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "DateIndex",
                    "KeySchema": [
                        {"AttributeName": "table_id", "KeyType": "HASH"},
                        {"AttributeName": "completed_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("✅ OrderHistory 테이블 생성 완료")
    except client.exceptions.ResourceInUseException:
        print("⏭️  OrderHistory 테이블 이미 존재")


def main():
    """모든 테이블 생성."""
    print("🚀 DynamoDB 테이블 생성 시작...")
    print("   Endpoint: http://localhost:8000")
    print()

    client = get_dynamodb_client()

    create_store_table(client)
    create_admin_user_table(client)
    create_table_table(client)
    create_table_session_table(client)
    create_order_table(client)
    create_order_history_table(client)

    print()
    print("🎉 테이블 생성 완료!")


if __name__ == "__main__":
    main()
