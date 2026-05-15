"""매장 서비스."""

from fastapi import HTTPException, status

from app.repositories.store_repository import StoreRepository


class StoreService:
    """매장 비즈니스 로직."""

    def __init__(self):
        self._store_repo = StoreRepository()

    def get_store(self, store_id: str) -> dict:
        """매장 정보 조회."""
        store = self._store_repo.get_by_id(store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="매장을 찾을 수 없습니다",
            )
        return store
