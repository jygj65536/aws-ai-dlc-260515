"""로컬 개발용 시드 데이터.

인메모리 저장소에 테스트 데이터를 삽입합니다.
서버 시작 시 자동 실행됩니다.
"""

from passlib.context import CryptContext

from app.core.storage import get_table

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

STORE_ID = "store-001"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
TABLE_1_NUMBER = 1
TABLE_1_PASSWORD = "1111"
TABLE_2_NUMBER = 2
TABLE_2_PASSWORD = "2222"


def seed() -> None:
    """시드 데이터 삽입."""
    _seed_store()
    _seed_admin()
    _seed_tables()
    _seed_categories_and_menus()
    print("🌱 시드 데이터 로드 완료")
    print(f"   매장 ID: {STORE_ID}")
    print(f"   관리자: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
    print(f"   테이블 1: 번호={TABLE_1_NUMBER}, 비밀번호={TABLE_1_PASSWORD}")
    print(f"   테이블 2: 번호={TABLE_2_NUMBER}, 비밀번호={TABLE_2_PASSWORD}")


def _seed_store():
    table = get_table("Store")
    table.put_item(Item={
        "store_id": STORE_ID,
        "name": "맛있는 식당",
        "created_at": "2026-01-01T00:00:00Z",
    })


def _seed_admin():
    table = get_table("AdminUser")
    table.put_item(Item={
        "store_id": STORE_ID,
        "username": ADMIN_USERNAME,
        "password_hash": pwd_context.hash(ADMIN_PASSWORD),
        "login_attempts": 0,
        "locked_until": None,
        "created_at": "2026-01-01T00:00:00Z",
    })


def _seed_tables():
    table = get_table("Table")
    table.put_item(Item={
        "store_id": STORE_ID,
        "table_id": "table-001",
        "table_number": TABLE_1_NUMBER,
        "password_hash": pwd_context.hash(TABLE_1_PASSWORD),
        "current_session_id": None,
        "created_at": "2026-01-01T00:00:00Z",
    })
    table.put_item(Item={
        "store_id": STORE_ID,
        "table_id": "table-002",
        "table_number": TABLE_2_NUMBER,
        "password_hash": pwd_context.hash(TABLE_2_PASSWORD),
        "current_session_id": None,
        "created_at": "2026-01-01T00:00:00Z",
    })


def _seed_categories_and_menus():
    cat_table = get_table("Category")
    menu_table = get_table("MenuItem")

    # 카테고리
    cat_table.put_item(Item={
        "store_id": STORE_ID,
        "category_id": "cat-001",
        "name": "메인 메뉴",
        "sort_order": 1,
        "created_at": "2026-01-01T00:00:00Z",
    })
    cat_table.put_item(Item={
        "store_id": STORE_ID,
        "category_id": "cat-002",
        "name": "사이드",
        "sort_order": 2,
        "created_at": "2026-01-01T00:00:00Z",
    })
    cat_table.put_item(Item={
        "store_id": STORE_ID,
        "category_id": "cat-003",
        "name": "음료",
        "sort_order": 3,
        "created_at": "2026-01-01T00:00:00Z",
    })

    # 메뉴
    menus = [
        {"menu_id": "menu-001", "category_id": "cat-001", "name": "김치찌개", "price": 9000, "description": "돼지고기 김치찌개", "sort_order": 1},
        {"menu_id": "menu-002", "category_id": "cat-001", "name": "된장찌개", "price": 8000, "description": "두부 된장찌개", "sort_order": 2},
        {"menu_id": "menu-003", "category_id": "cat-001", "name": "제육볶음", "price": 11000, "description": "매콤 제육볶음", "sort_order": 3},
        {"menu_id": "menu-004", "category_id": "cat-001", "name": "불고기", "price": 12000, "description": "소불고기 정식", "sort_order": 4},
        {"menu_id": "menu-005", "category_id": "cat-002", "name": "계란말이", "price": 5000, "description": "부드러운 계란말이", "sort_order": 1},
        {"menu_id": "menu-006", "category_id": "cat-002", "name": "김치전", "price": 6000, "description": "바삭한 김치전", "sort_order": 2},
        {"menu_id": "menu-007", "category_id": "cat-003", "name": "콜라", "price": 2000, "description": "", "sort_order": 1},
        {"menu_id": "menu-008", "category_id": "cat-003", "name": "사이다", "price": 2000, "description": "", "sort_order": 2},
    ]
    for menu in menus:
        menu_table.put_item(Item={
            "store_id": STORE_ID,
            "menu_id": menu["menu_id"],
            "category_id": menu["category_id"],
            "name": menu["name"],
            "price": menu["price"],
            "description": menu["description"],
            "image_url": None,
            "sort_order": menu["sort_order"],
            "is_available": True,
            "created_at": "2026-01-01T00:00:00Z",
        })
