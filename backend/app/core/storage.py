"""SQLite 기반 저장소 - DynamoDB 대체 (로컬 개발용).

Docker나 AWS 없이 로컬에서 바로 실행 가능.
데이터가 파일에 저장되어 서버 재시작 후에도 유지됨.
"""

import json
import os
import sqlite3
from copy import deepcopy
from pathlib import Path
from threading import Lock

# SQLite DB 파일 경로 (프로젝트 루트의 backend/data/ 디렉토리)
_DB_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_DB_PATH = _DB_DIR / "local.db"


def _get_connection() -> sqlite3.Connection:
    """SQLite 연결 반환."""
    _DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# 모듈 레벨 연결 (싱글톤)
_conn: sqlite3.Connection | None = None
_lock = Lock()


def _db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = _get_connection()
    return _conn


class SQLiteTable:
    """DynamoDB 테이블을 모방하는 SQLite 기반 저장소.

    각 테이블은 SQLite의 별도 테이블로 저장.
    아이템은 JSON으로 직렬화하여 저장.
    PK/SK 기반 조회, GSI 시뮬레이션 지원.
    """

    def __init__(self, table_name: str, pk_name: str, sk_name: str | None = None):
        self._table_name = table_name
        self._pk_name = pk_name
        self._sk_name = sk_name
        self._ensure_table()

    def _ensure_table(self):
        """SQLite 테이블 생성 (없으면)."""
        conn = _db()
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS "{self._table_name}" (
                pk TEXT NOT NULL,
                sk TEXT NOT NULL DEFAULT '__default__',
                data TEXT NOT NULL,
                PRIMARY KEY (pk, sk)
            )
        """)
        conn.commit()

    def put_item(self, Item: dict) -> None:
        """아이템 저장 (upsert)."""
        pk = str(Item[self._pk_name])
        sk = str(Item[self._sk_name]) if self._sk_name else "__default__"
        data_json = json.dumps(Item, ensure_ascii=False, default=str)
        conn = _db()
        with _lock:
            conn.execute(
                f'INSERT OR REPLACE INTO "{self._table_name}" (pk, sk, data) VALUES (?, ?, ?)',
                (pk, sk, data_json),
            )
            conn.commit()

    def get_item(self, Key: dict) -> dict:
        """아이템 단건 조회."""
        pk = str(Key[self._pk_name])
        sk = str(Key[self._sk_name]) if self._sk_name else "__default__"
        conn = _db()
        with _lock:
            cursor = conn.execute(
                f'SELECT data FROM "{self._table_name}" WHERE pk = ? AND sk = ?',
                (pk, sk),
            )
            row = cursor.fetchone()
        if row:
            return {"Item": json.loads(row[0])}
        return {}

    def delete_item(self, Key: dict) -> None:
        """아이템 삭제."""
        pk = str(Key[self._pk_name])
        sk = str(Key[self._sk_name]) if self._sk_name else "__default__"
        conn = _db()
        with _lock:
            conn.execute(
                f'DELETE FROM "{self._table_name}" WHERE pk = ? AND sk = ?',
                (pk, sk),
            )
            conn.commit()

    def update_item(
        self,
        Key: dict,
        UpdateExpression: str = "",
        ExpressionAttributeValues: dict | None = None,
        ExpressionAttributeNames: dict | None = None,
        ReturnValues: str = "NONE",
        **kwargs,
    ) -> dict:
        """아이템 업데이트 (간단한 SET/REMOVE 지원)."""
        pk = str(Key[self._pk_name])
        sk = str(Key[self._sk_name]) if self._sk_name else "__default__"
        attr_names = ExpressionAttributeNames or {}
        attr_values = ExpressionAttributeValues or {}

        with _lock:
            conn = _db()
            cursor = conn.execute(
                f'SELECT data FROM "{self._table_name}" WHERE pk = ? AND sk = ?',
                (pk, sk),
            )
            row = cursor.fetchone()
            if row:
                item = json.loads(row[0])
            else:
                item = deepcopy(Key)

            # UpdateExpression 파싱
            expr = UpdateExpression.strip()

            # SET 처리
            if "SET" in expr:
                set_part = expr.split("SET", 1)[1]
                if "REMOVE" in set_part:
                    set_part = set_part.split("REMOVE")[0]
                assignments = [a.strip() for a in set_part.split(",")]
                for assignment in assignments:
                    if "=" not in assignment:
                        continue
                    left, right = assignment.split("=", 1)
                    left = left.strip()
                    right = right.strip()
                    field = attr_names.get(left, left)

                    if "+" in right:
                        parts = [p.strip() for p in right.split("+")]
                        base_field = attr_names.get(parts[0], parts[0])
                        current_val = item.get(base_field, 0)
                        delta = attr_values.get(parts[1], 0)
                        item[field] = _to_number(current_val) + _to_number(delta)
                    elif right.startswith(":"):
                        item[field] = attr_values[right]
                    else:
                        item[field] = right

            # REMOVE 처리
            if "REMOVE" in expr:
                remove_part = expr.split("REMOVE", 1)[1].strip()
                if "SET" in remove_part:
                    remove_part = remove_part.split("SET")[0]
                fields = [f.strip() for f in remove_part.split(",")]
                for field in fields:
                    real_field = attr_names.get(field, field)
                    item.pop(real_field, None)

            # 저장
            data_json = json.dumps(item, ensure_ascii=False, default=str)
            conn.execute(
                f'INSERT OR REPLACE INTO "{self._table_name}" (pk, sk, data) VALUES (?, ?, ?)',
                (pk, sk, data_json),
            )
            conn.commit()

        result = {"Attributes": deepcopy(item)} if ReturnValues != "NONE" else {}
        return result

    def query(
        self,
        KeyConditionExpression=None,
        FilterExpression=None,
        IndexName: str | None = None,
        ScanIndexForward: bool = True,
        Limit: int | None = None,
        Select: str | None = None,
        **kwargs,
    ) -> dict:
        """쿼리 (PK 기반 조회 시뮬레이션)."""
        conn = _db()
        with _lock:
            cursor = conn.execute(f'SELECT data FROM "{self._table_name}"')
            all_items = [json.loads(row[0]) for row in cursor.fetchall()]

        # KeyConditionExpression 필터링
        if KeyConditionExpression:
            all_items = [
                item for item in all_items
                if KeyConditionExpression.evaluate(item)
            ]

        # FilterExpression 필터링
        if FilterExpression:
            all_items = [
                item for item in all_items
                if FilterExpression.evaluate(item)
            ]

        # 정렬
        sk_field = self._sk_name or "created_at"
        if IndexName:
            sk_field = _guess_gsi_sk(IndexName)
        all_items.sort(
            key=lambda x: str(x.get(sk_field, "")),
            reverse=not ScanIndexForward,
        )

        if Limit:
            all_items = all_items[:Limit]

        if Select == "COUNT":
            return {"Count": len(all_items), "Items": []}

        return {"Items": all_items, "Count": len(all_items)}

    def batch_writer(self):
        """배치 라이터."""
        return _BatchWriter(self)

    def scan(self, **kwargs) -> dict:
        """전체 스캔."""
        conn = _db()
        with _lock:
            cursor = conn.execute(f'SELECT data FROM "{self._table_name}"')
            all_items = [json.loads(row[0]) for row in cursor.fetchall()]
        return {"Items": all_items, "Count": len(all_items)}


class _BatchWriter:
    """배치 라이터 컨텍스트 매니저."""

    def __init__(self, table: SQLiteTable):
        self._table = table

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def put_item(self, Item: dict) -> None:
        self._table.put_item(Item=Item)

    def delete_item(self, Key: dict) -> None:
        self._table.delete_item(Key=Key)


def _to_number(val) -> int | float:
    """값을 숫자로 변환."""
    if isinstance(val, (int, float)):
        return val
    try:
        return int(val)
    except (ValueError, TypeError):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0


def _guess_gsi_sk(index_name: str) -> str:
    """GSI 이름에서 SK 필드 추정."""
    mapping = {
        "StoreOrderIndex": "created_at",
        "TableNumberIndex": "table_number",
        "DateIndex": "completed_at",
        "CategoryIndex": "category_id",
    }
    return mapping.get(index_name, "created_at")


# --- Condition Expression 클래스 (boto3 호환) ---


class _Condition:
    """조건 표현식 기본 클래스."""

    def evaluate(self, item: dict) -> bool:
        raise NotImplementedError

    def __and__(self, other):
        return _AndCondition(self, other)

    def __or__(self, other):
        return _OrCondition(self, other)


class _EqCondition(_Condition):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    def evaluate(self, item: dict) -> bool:
        item_val = item.get(self.field)
        # 숫자 비교 지원
        if isinstance(self.value, (int, float)):
            try:
                return _to_number(item_val) == self.value
            except (ValueError, TypeError):
                pass
        return item_val == self.value


class _GtCondition(_Condition):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    def evaluate(self, item: dict) -> bool:
        item_val = item.get(self.field)
        if item_val is None:
            return False
        return str(item_val) > str(self.value)


class _GteCondition(_Condition):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    def evaluate(self, item: dict) -> bool:
        item_val = item.get(self.field)
        if item_val is None:
            return False
        return str(item_val) >= str(self.value)


class _LteCondition(_Condition):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    def evaluate(self, item: dict) -> bool:
        item_val = item.get(self.field)
        if item_val is None:
            return False
        return str(item_val) <= str(self.value)


class _BetweenCondition(_Condition):
    def __init__(self, field: str, low, high):
        self.field = field
        self.low = low
        self.high = high

    def evaluate(self, item: dict) -> bool:
        item_val = item.get(self.field)
        if item_val is None:
            return False
        return str(self.low) <= str(item_val) <= str(self.high)


class _AndCondition(_Condition):
    def __init__(self, left: _Condition, right: _Condition):
        self.left = left
        self.right = right

    def evaluate(self, item: dict) -> bool:
        return self.left.evaluate(item) and self.right.evaluate(item)


class _OrCondition(_Condition):
    def __init__(self, left: _Condition, right: _Condition):
        self.left = left
        self.right = right

    def evaluate(self, item: dict) -> bool:
        return self.left.evaluate(item) or self.right.evaluate(item)


class _KeyHelper:
    """boto3 Key() 호환 헬퍼."""

    def __init__(self, field: str):
        self.field = field

    def eq(self, value) -> _Condition:
        return _EqCondition(self.field, value)

    def gt(self, value) -> _Condition:
        return _GtCondition(self.field, value)

    def gte(self, value) -> _Condition:
        return _GteCondition(self.field, value)

    def lte(self, value) -> _Condition:
        return _LteCondition(self.field, value)

    def between(self, low, high) -> _Condition:
        return _BetweenCondition(self.field, low, high)


class _AttrHelper:
    """boto3 Attr() 호환 헬퍼."""

    def __init__(self, field: str):
        self.field = field

    def eq(self, value) -> _Condition:
        return _EqCondition(self.field, value)

    def gt(self, value) -> _Condition:
        return _GtCondition(self.field, value)

    def gte(self, value) -> _Condition:
        return _GteCondition(self.field, value)

    def lte(self, value) -> _Condition:
        return _LteCondition(self.field, value)


def Key(field: str) -> _KeyHelper:
    """boto3.dynamodb.conditions.Key 대체."""
    return _KeyHelper(field)


def Attr(field: str) -> _AttrHelper:
    """boto3.dynamodb.conditions.Attr 대체."""
    return _AttrHelper(field)


# --- 테이블 레지스트리 ---

_tables: dict[str, SQLiteTable] = {}


def get_table(table_name: str) -> SQLiteTable:
    """테이블 인스턴스 반환 (없으면 생성)."""
    if table_name not in _tables:
        schema = {
            "Store": ("store_id", None),
            "AdminUser": ("store_id", "username"),
            "Table": ("store_id", "table_id"),
            "TableSession": ("table_id", "session_id"),
            "Order": ("session_id", "order_id"),
            "OrderHistory": ("table_id", "history_id"),
            "Category": ("store_id", "category_id"),
            "MenuItem": ("store_id", "menu_id"),
        }
        pk, sk = schema.get(table_name, ("id", None))
        _tables[table_name] = SQLiteTable(table_name=table_name, pk_name=pk, sk_name=sk)
    return _tables[table_name]


def reset_all_tables() -> None:
    """모든 테이블 초기화 (테스트용)."""
    conn = _db()
    with _lock:
        for table_name in list(_tables.keys()):
            conn.execute(f'DELETE FROM "{table_name}"')
        conn.commit()
    _tables.clear()


def get_db_path() -> str:
    """DB 파일 경로 반환."""
    return str(_DB_PATH)
