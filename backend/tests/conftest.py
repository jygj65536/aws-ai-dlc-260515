"""테스트 공통 fixtures."""

import os
from unittest.mock import patch

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.core.security import hash_password


@pytest.fixture(autouse=True)
def env_setup():
    """테스트 환경변수 설정."""
    os.environ["DYNAMODB_ENDPOINT_URL"] = "http://localhost:8000"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_EXPIRE_HOURS"] = "16"
    yield


@pytest.fixture
def mock_dynamodb():
    """moto를 사용한 DynamoDB 모킹."""
    with mock_aws():
        client = boto3.client("dynamodb", region_name="ap-northeast-2")

        # AdminUser 테이블
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

        # Table 테이블 + GSI
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

        # TableSession 테이블
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

        resource = boto3.resource("dynamodb", region_name="ap-northeast-2")

        # 시드 데이터: 관리자
        admin_table = resource.Table("AdminUser")
        admin_table.put_item(
            Item={
                "store_id": "store-001",
                "username": "admin",
                "password_hash": hash_password("admin1234"),
                "login_attempts": 0,
                "created_at": "2026-01-01T00:00:00Z",
            }
        )

        # 시드 데이터: 테이블
        table_table = resource.Table("Table")
        table_table.put_item(
            Item={
                "store_id": "store-001",
                "table_id": "table-uuid-001",
                "table_number": 1,
                "password_hash": hash_password("1234"),
                "current_session_id": None,
                "created_at": "2026-01-01T00:00:00Z",
            }
        )

        yield resource


@pytest.fixture
def client(mock_dynamodb):
    """FastAPI TestClient with mocked DynamoDB."""
    with patch("app.core.dynamodb.dynamodb_resource", mock_dynamodb):
        with patch(
            "app.repositories.admin_user_repository.dynamodb_resource", mock_dynamodb
        ):
            with patch(
                "app.repositories.table_repository.dynamodb_resource", mock_dynamodb
            ):
                with patch(
                    "app.repositories.session_repository.dynamodb_resource",
                    mock_dynamodb,
                ):
                    from app.main import app

                    yield TestClient(app)
