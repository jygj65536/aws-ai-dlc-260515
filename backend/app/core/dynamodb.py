"""DynamoDB 클라이언트 모듈.

로컬 개발 시 인메모리 저장소를 사용하여 Docker/AWS 없이 실행 가능.
USE_DYNAMODB=true 환경변수 설정 시 실제 DynamoDB 연결.
"""

import os

from app.config import get_settings

# 인메모리 모드 여부 (기본: 인메모리)
_USE_DYNAMODB = os.environ.get("USE_DYNAMODB", "false").lower() == "true"


class _InMemoryResource:
    """인메모리 저장소를 DynamoDB resource처럼 사용할 수 있는 래퍼."""

    def Table(self, table_name: str):
        from app.core.storage import get_table
        return get_table(table_name)


def get_dynamodb_resource():
    """DynamoDB 리소스 객체 반환.

    - USE_DYNAMODB=true: 실제 DynamoDB (Local 또는 AWS)
    - USE_DYNAMODB=false (기본): 인메모리 저장소
    """
    if _USE_DYNAMODB:
        import boto3
        settings = get_settings()
        return boto3.resource(
            "dynamodb",
            region_name=settings.aws_region,
            endpoint_url=settings.dynamodb_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
    return _InMemoryResource()


def get_dynamodb_client():
    """DynamoDB 클라이언트 객체 반환 (테이블 생성 등 관리 작업용)."""
    if _USE_DYNAMODB:
        import boto3
        settings = get_settings()
        return boto3.client(
            "dynamodb",
            region_name=settings.aws_region,
            endpoint_url=settings.dynamodb_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
    # 인메모리 모드에서는 클라이언트 불필요
    return None
