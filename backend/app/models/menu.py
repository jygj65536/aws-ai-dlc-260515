"""메뉴/카테고리 관련 Pydantic 스키마."""

from pydantic import BaseModel, Field


# --- 카테고리 ---

class CreateCategoryRequest(BaseModel):
    store_id: str
    name: str = Field(..., min_length=1, max_length=30)
    sort_order: int = Field(default=0, ge=0)


class UpdateCategoryRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=30)
    sort_order: int | None = Field(None, ge=0)


class CategoryResponse(BaseModel):
    category_id: str
    store_id: str
    name: str
    sort_order: int


# --- 메뉴 ---

class CreateMenuRequest(BaseModel):
    store_id: str
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(..., ge=100, le=1000000)
    description: str = Field(default="", max_length=200)
    category_id: str
    sort_order: int = Field(default=0, ge=0)


class UpdateMenuRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    price: int | None = Field(None, ge=100, le=1000000)
    description: str | None = Field(None, max_length=200)
    category_id: str | None = None
    sort_order: int | None = Field(None, ge=0)
    is_available: bool | None = None


class MenuItemResponse(BaseModel):
    menu_id: str
    store_id: str
    category_id: str
    name: str
    price: int
    description: str
    sort_order: int
    is_available: bool


class MenuListResponse(BaseModel):
    categories: list[dict]
