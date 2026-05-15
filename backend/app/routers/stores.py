"""매장 API 엔드포인트."""

from fastapi import APIRouter

from app.services.store_service import StoreService

router = APIRouter()


def _get_service() -> StoreService:
    return StoreService()


@router.get(
    "/stores/{store_id}",
    summary="매장 정보 조회",
)
async def get_store(store_id: str):
    """매장 정보 조회."""
    service = _get_service()
    return service.get_store(store_id)
