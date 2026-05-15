"""애플리케이션 설정 모듈."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """환경변수 기반 애플리케이션 설정."""

    # 앱 설정
    app_name: str = "Table Order API"
    debug: bool = False

    # DynamoDB 설정
    aws_region: str = "ap-northeast-2"
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    dynamodb_endpoint_url: str = "http://localhost:8000"

    # JWT 설정
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 16

    # 세션 설정
    session_expire_hours: int = 4

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    """설정 싱글톤 반환."""
    return Settings()
