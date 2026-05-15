"""DynamoDB 클라이언트 초기화 모듈."""

import boto3
from app.config import settings


def get_dynamodb_resource():
    """DynamoDB 리소스 객체를 반환한다."""
    return boto3.resource(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def get_dynamodb_client():
    """DynamoDB 클라이언트 객체를 반환한다."""
    return boto3.client(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


# 싱글턴 인스턴스
dynamodb_resource = get_dynamodb_resource()
