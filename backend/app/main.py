"""FastAPI 애플리케이션 진입점."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth

app = FastAPI(
    title="Table Order Service",
    description="테이블 오더 서비스 API",
    version="1.0.0",
)

# CORS 설정 (로컬 개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])


@app.get("/health", tags=["Health"])
async def health_check():
    """헬스 체크 엔드포인트."""
    return {"status": "ok", "env": settings.app_env}
