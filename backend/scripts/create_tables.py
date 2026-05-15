"""DynamoDB 로컬 테이블 생성 스크립트.

사용법: python -m scripts.create_tables
"""

import boto3
from app.config import settings


def get_client():
    return boto3.client(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def create_store_table(client):
    """Store 테이블 생성."""
    client.create_table(
        TableName="Store",
        KeySchema=[{"AttributeName": "store_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "store_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    print("✅ Store 테이블 생성 완료")


def create_admin_user_table(client):
    """AdminUser 테이블 생성."""
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


def create_table_table(client):
    """Table 테이블 생성 (GSI: TableNumberIndex)."""
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
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("✅ Table 테이블 생성 완료 (GSI: TableNumberIndex)")


def create_table_session_table(client):
    """TableSession 테이블 생성."""
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
        BillingMode="PAY_PER_REQUEST",
    )
    print("✅ TableSession 테이블 생성 완료")


def main():
    client = get_client()

    # 기존 테이블 목록 확인
    existing = client.list_tables()["TableNames"]

    tables_to_create = [
        ("Store", create_store_table),
        ("AdminUser", create_admin_user_table),
        ("Table", create_table_table),
        ("TableSession", create_table_session_table),
    ]

    for table_name, create_fn in tables_to_create:
        if table_name in existing:
            print(f"⏭️  {table_name} 테이블 이미 존재 (건너뜀)")
        else:
            create_fn(client)

    print("\n🎉 모든 테이블 생성 완료!")


if __name__ == "__main__":
    main()
