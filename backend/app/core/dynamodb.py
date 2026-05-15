"""DynamoDB 클라이언트 초기화 모듈."""

import boto3
from boto3.resources.base import ServiceResource

from app.config import get_settings


def get_dynamodb_resource() -> ServiceResource:
    """DynamoDB 리소스 객체 반환."""
    settings = get_settings()
    return boto3.resource(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def get_dynamodb_client():
    """DynamoDB 클라이언트 객체 반환 (테이블 생성 등 관리 작업용)."""
    settings = get_settings()
    return boto3.client(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=settings.dynamodb_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
