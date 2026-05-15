"""메뉴/카테고리 API 엔드포인트."""

from fastapi import APIRouter, Query

from app.models.menu import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateMenuRequest,
    MenuItemResponse,
    MenuListResponse,
    UpdateCategoryRequest,
    UpdateMenuRequest,
)
from app.services.menu_service import MenuService

router = APIRouter()


def _get_service() -> MenuService:
    return MenuService()


# --- 메뉴 ---


@router.get(
    "/menus",
    response_model=MenuListResponse,
    summary="메뉴 목록 조회 (카테고리 포함)",
)
async def get_menus(store_id: str = Query(..., description="매장 ID")):
    """메뉴 목록 조회 (US-1).

    카테고리별로 그룹핑된 메뉴 목록을 반환합니다.
    판매 가능한 메뉴만 포함됩니다.
    """
    service = _get_service()
    return service.get_menus(store_id)


@router.post(
    "/menus",
    response_model=MenuItemResponse,
    status_code=201,
    summary="메뉴 등록",
)
async def create_menu(request: CreateMenuRequest):
    """메뉴 등록 (US-8)."""
    service = _get_service()
    result = service.create_menu(request)
    return MenuItemResponse(
        menu_id=result["menu_id"],
        store_id=result["store_id"],
        category_id=result["category_id"],
        name=result["name"],
        price=result["price"],
        description=result["description"],
        sort_order=result["sort_order"],
        is_available=result["is_available"],
    )


@router.put(
    "/menus/{menu_id}",
    response_model=MenuItemResponse,
    summary="메뉴 수정",
)
async def update_menu(
    menu_id: str,
    request: UpdateMenuRequest,
    store_id: str = Query(..., description="매장 ID"),
):
    """메뉴 수정 (US-8)."""
    service = _get_service()
    result = service.update_menu(store_id, menu_id, request)
    return MenuItemResponse(
        menu_id=result["menu_id"],
        store_id=result["store_id"],
        category_id=result["category_id"],
        name=result["name"],
        price=int(result["price"]),
        description=result.get("description", ""),
        sort_order=int(result.get("sort_order", 0)),
        is_available=result.get("is_available", True),
    )


@router.delete("/menus/{menu_id}", summary="메뉴 삭제")
async def delete_menu(
    menu_id: str,
    store_id: str = Query(..., description="매장 ID"),
):
    """메뉴 삭제 (US-8)."""
    service = _get_service()
    service.delete_menu(store_id, menu_id)
    return {"success": True}


# --- 카테고리 ---


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
    summary="카테고리 목록 조회",
)
async def get_categories(store_id: str = Query(..., description="매장 ID")):
    """카테고리 목록 조회."""
    service = _get_service()
    categories = service.get_categories(store_id)
    return [
        CategoryResponse(
            category_id=c["category_id"],
            store_id=c["store_id"],
            name=c["name"],
            sort_order=int(c.get("sort_order", 0)),
        )
        for c in categories
    ]


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=201,
    summary="카테고리 등록",
)
async def create_category(request: CreateCategoryRequest):
    """카테고리 등록."""
    service = _get_service()
    result = service.create_category(request)
    return CategoryResponse(
        category_id=result["category_id"],
        store_id=result["store_id"],
        name=result["name"],
        sort_order=result["sort_order"],
    )


@router.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="카테고리 수정",
)
async def update_category(
    category_id: str,
    request: UpdateCategoryRequest,
    store_id: str = Query(..., description="매장 ID"),
):
    """카테고리 수정."""
    service = _get_service()
    result = service.update_category(store_id, category_id, request)
    return CategoryResponse(
        category_id=result["category_id"],
        store_id=result["store_id"],
        name=result["name"],
        sort_order=int(result.get("sort_order", 0)),
    )


@router.delete("/categories/{category_id}", summary="카테고리 삭제")
async def delete_category(
    category_id: str,
    store_id: str = Query(..., description="매장 ID"),
):
    """카테고리 삭제."""
    service = _get_service()
    service.delete_category(store_id, category_id)
    return {"success": True}
