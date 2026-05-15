"""FastAPI 애플리케이션 진입점."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, orders, sse

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="테이블 주문 시스템 API",
)

# CORS 설정 (개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(sse.router, prefix="/api", tags=["sse"])


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트."""
    return {"status": "healthy"}
