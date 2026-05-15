"""FastAPI 애플리케이션 진입점."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, menus, orders, sse, stores, tables

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 이벤트."""
    # 시작 시 시드 데이터 로드 (인메모리 모드)
    import os
    if os.environ.get("USE_DYNAMODB", "false").lower() != "true":
        from app.core.seed_data import seed
        seed()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="테이블 주문 시스템 API",
    lifespan=lifespan,
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
app.include_router(stores.router, prefix="/api", tags=["stores"])
app.include_router(tables.router, prefix="/api", tags=["tables"])
app.include_router(menus.router, prefix="/api", tags=["menus"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(sse.router, prefix="/api", tags=["sse"])


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트."""
    return {"status": "healthy"}
