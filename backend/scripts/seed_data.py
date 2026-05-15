"""테스트용 초기 데이터 시드 스크립트.

사용법: python -m scripts.seed_data

생성 데이터:
- 매장 1개 (store_id: "store-001")
- 관리자 1명 (username: "admin", password: "admin1234")
- 테이블 2개 (table_number: 1, 2, password: "1234")
"""

import uuid
from datetime import datetime, timezone

import boto3

from app.config import settings
from app.core.security import hash_password


def get_resource():
    return boto3.resource(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def main():
    dynamodb = get_resource()
    now = datetime.now(timezone.utc).isoformat()

    store_id = "store-001"

    # 1. Store 생성
    store_table = dynamodb.Table("Store")
    store_table.put_item(
        Item={
            "store_id": store_id,
            "name": "테스트 매장",
            "created_at": now,
        }
    )
    print(f"✅ Store 생성: {store_id} (테스트 매장)")

    # 2. AdminUser 생성
    admin_table = dynamodb.Table("AdminUser")
    admin_table.put_item(
        Item={
            "store_id": store_id,
            "username": "admin",
            "password_hash": hash_password("admin1234"),
            "login_attempts": 0,
            "created_at": now,
        }
    )
    print("✅ AdminUser 생성: admin / admin1234")

    # 3. Table 생성 (2개)
    table_resource = dynamodb.Table("Table")
    for table_number in [1, 2]:
        table_id = str(uuid.uuid4())
        table_resource.put_item(
            Item={
                "store_id": store_id,
                "table_id": table_id,
                "table_number": table_number,
                "password_hash": hash_password("1234"),
                "current_session_id": None,
                "created_at": now,
            }
        )
        print(f"✅ Table 생성: #{table_number} (table_id: {table_id}, password: 1234)")

    print("\n🎉 시드 데이터 생성 완료!")
    print(f"   매장 ID: {store_id}")
    print("   관리자: admin / admin1234")
    print("   테이블: #1, #2 / 비밀번호: 1234")


if __name__ == "__main__":
    main()
