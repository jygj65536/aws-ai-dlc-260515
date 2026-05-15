"""메뉴/카테고리 비즈니스 로직 서비스."""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.menu import (
    CreateCategoryRequest,
    CreateMenuRequest,
    UpdateCategoryRequest,
    UpdateMenuRequest,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_repository import MenuRepository


class MenuService:
    """메뉴/카테고리 비즈니스 로직."""

    def __init__(self):
        self._menu_repo = MenuRepository()
        self._category_repo = CategoryRepository()

    def get_menus(self, store_id: str) -> dict:
        """메뉴 목록 조회 (카테고리별 그룹핑)."""
        categories = self._category_repo.get_by_store(store_id)
        menus = self._menu_repo.get_by_store(store_id, available_only=True)

        # 카테고리별 그룹핑
        result = []
        for cat in categories:
            cat_menus = [
                {
                    "menu_id": m["menu_id"],
                    "name": m["name"],
                    "price": int(m["price"]),
                    "description": m.get("description", ""),
                    "sort_order": int(m.get("sort_order", 0)),
                    "is_available": m.get("is_available", True),
                }
                for m in menus
                if m.get("category_id") == cat["category_id"]
            ]
            result.append({
                "category_id": cat["category_id"],
                "name": cat["name"],
                "sort_order": int(cat.get("sort_order", 0)),
                "items": cat_menus,
            })

        return {"categories": result}

    def create_menu(self, request: CreateMenuRequest) -> dict:
        """메뉴 등록."""
        # 카테고리 존재 확인
        category = self._category_repo.get_by_id(request.store_id, request.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 카테고리입니다",
            )

        menu_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        menu_data = {
            "store_id": request.store_id,
            "menu_id": menu_id,
            "category_id": request.category_id,
            "name": request.name,
            "price": request.price,
            "description": request.description,
            "image_url": None,
            "sort_order": request.sort_order,
            "is_available": True,
            "created_at": now,
        }

        self._menu_repo.save(menu_data)
        return menu_data

    def update_menu(self, store_id: str, menu_id: str, request: UpdateMenuRequest) -> dict:
        """메뉴 수정."""
        menu = self._menu_repo.get_by_id(store_id, menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="메뉴를 찾을 수 없습니다",
            )

        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        if not updates:
            return menu

        updated = self._menu_repo.update(store_id, menu_id, updates)
        return updated

    def delete_menu(self, store_id: str, menu_id: str) -> None:
        """메뉴 삭제."""
        menu = self._menu_repo.get_by_id(store_id, menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="메뉴를 찾을 수 없습니다",
            )
        self._menu_repo.delete(store_id, menu_id)

    # --- 카테고리 ---

    def get_categories(self, store_id: str) -> list[dict]:
        """카테고리 목록 조회."""
        return self._category_repo.get_by_store(store_id)

    def create_category(self, request: CreateCategoryRequest) -> dict:
        """카테고리 등록."""
        category_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        category_data = {
            "store_id": request.store_id,
            "category_id": category_id,
            "name": request.name,
            "sort_order": request.sort_order,
            "created_at": now,
        }

        self._category_repo.save(category_data)
        return category_data

    def update_category(self, store_id: str, category_id: str, request: UpdateCategoryRequest) -> dict:
        """카테고리 수정."""
        category = self._category_repo.get_by_id(store_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="카테고리를 찾을 수 없습니다",
            )

        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        if not updates:
            return category

        updated = self._category_repo.update(store_id, category_id, updates)
        return updated

    def delete_category(self, store_id: str, category_id: str) -> None:
        """카테고리 삭제."""
        category = self._category_repo.get_by_id(store_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="카테고리를 찾을 수 없습니다",
            )
        self._category_repo.delete(store_id, category_id)
