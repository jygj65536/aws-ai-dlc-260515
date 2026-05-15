"""애플리케이션 설정 모듈."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """환경변수 기반 애플리케이션 설정."""

    # AWS DynamoDB
    aws_region: str = "ap-northeast-2"
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    dynamodb_endpoint_url: str = "http://localhost:8000"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 16

    # Application
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8080

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
