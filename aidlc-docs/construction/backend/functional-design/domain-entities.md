# Domain Entities - Backend

## 데이터 저장소 설계

### 구현 방식
- **저장소**: SQLite (파일: `backend/data/local.db`)
- **인터페이스**: DynamoDB API 호환 래퍼 (`app/core/storage.py`)
- **구조**: 각 엔티티가 별도 SQLite 테이블, 데이터는 JSON으로 직렬화
- **전환**: `USE_DYNAMODB=true` 환경변수로 실제 DynamoDB 사용 가능

### SQLite 내부 구조 (모든 테이블 공통)
```sql
CREATE TABLE "{table_name}" (
    pk TEXT NOT NULL,
    sk TEXT NOT NULL DEFAULT '__default__',
    data TEXT NOT NULL,  -- JSON 직렬화된 엔티티 데이터
    PRIMARY KEY (pk, sk)
);
```

---

## 1. Store (매장)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| store_id | String (UUID) | PK | 매장 고유 식별자 |
| name | String | - | 매장명 |
| created_at | String (ISO 8601) | - | 생성 시각 |

---

## 2. AdminUser (관리자)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| store_id | String | PK | 매장 ID |
| username | String | SK | 사용자명 |
| password_hash | String | - | bcrypt 해시된 비밀번호 |
| login_attempts | Number | - | 연속 로그인 실패 횟수 |
| locked_until | String (ISO 8601) | - | 잠금 해제 시각 (null이면 미잠금) |
| created_at | String (ISO 8601) | - | 생성 시각 |

---

## 3. Table (테이블)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| store_id | String | PK | 매장 ID |
| table_id | String (UUID) | SK | 테이블 고유 ID |
| table_number | Number | - | 테이블 번호 |
| password_hash | String | - | 테이블 비밀번호 (bcrypt) |
| current_session_id | String | - | 현재 활성 세션 ID (null이면 비어있음) |
| created_at | String (ISO 8601) | - | 생성 시각 |

**GSI**: `TableNumberIndex` — PK: store_id, SK: table_number (테이블 번호로 조회용)

---

## 4. TableSession (테이블 세션)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| table_id | String | PK | 테이블 ID |
| session_id | String (UUID) | SK | 세션 고유 ID |
| store_id | String | - | 매장 ID |
| status | String | - | "active" / "expired" / "completed" |
| started_at | String (ISO 8601) | - | 세션 시작 시각 |
| expires_at | String (ISO 8601) | - | 만료 예정 시각 (시작 + 4시간) |
| completed_at | String (ISO 8601) | - | 이용 완료 시각 (null이면 진행중) |
| total_amount | Number | - | 총 주문 금액 |

---

## 5. Category (카테고리)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| store_id | String | PK | 매장 ID |
| category_id | String (UUID) | SK | 카테고리 고유 ID |
| name | String | - | 카테고리명 |
| sort_order | Number | - | 정렬 순서 |
| created_at | String (ISO 8601) | - | 생성 시각 |

---

## 6. MenuItem (메뉴 항목)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| store_id | String | PK | 매장 ID |
| menu_id | String (UUID) | SK | 메뉴 고유 ID |
| category_id | String | - | 소속 카테고리 ID |
| name | String | - | 메뉴명 |
| price | Number | - | 가격 (원) |
| description | String | - | 메뉴 설명 |
| image_url | String | - | 이미지 URL (MVP에서 미사용, 향후 확장용) |
| sort_order | Number | - | 정렬 순서 |
| is_available | Boolean | - | 판매 가능 여부 |
| created_at | String (ISO 8601) | - | 생성 시각 |

**GSI**: `CategoryIndex` — PK: store_id, SK: category_id (카테고리별 메뉴 조회용)

---

## 7. Order (주문)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| session_id | String | PK | 세션 ID |
| order_id | String (UUID) | SK | 주문 고유 ID |
| store_id | String | - | 매장 ID |
| table_id | String | - | 테이블 ID |
| order_number | Number | - | 주문 번호 (매장 내 순번) |
| status | String | - | "pending" / "preparing" / "completed" |
| items | List | - | 주문 항목 리스트 (임베디드) |
| total_amount | Number | - | 총 주문 금액 |
| created_at | String (ISO 8601) | - | 주문 시각 |

**items 구조** (임베디드 리스트):
```json
[
  {
    "menu_id": "uuid",
    "name": "김치찌개",
    "quantity": 2,
    "price": 9000,
    "subtotal": 18000
  }
]
```

**GSI**: `StoreOrderIndex` — PK: store_id, SK: created_at (매장별 최신 주문 조회용)

> **설계 결정**: OrderItem을 별도 테이블 대신 Order의 items 필드에 임베디드. 
> 이유: 주문 항목은 항상 주문과 함께 조회되며, 단독 조회 필요 없음. DynamoDB 단일 아이템 크기 제한(400KB) 내에서 충분.

---

## 8. OrderHistory (과거 주문 이력)

| 속성 | 타입 | 키 | 설명 |
|------|------|:---:|------|
| table_id | String | PK | 테이블 ID |
| history_id | String (UUID) | SK | 이력 고유 ID |
| store_id | String | - | 매장 ID |
| session_id | String | - | 원본 세션 ID |
| orders | List | - | 해당 세션의 전체 주문 리스트 |
| total_amount | Number | - | 세션 총 금액 |
| completed_at | String (ISO 8601) | - | 이용 완료 시각 |

**GSI**: `DateIndex` — PK: table_id, SK: completed_at (날짜별 조회용)

---

## 엔티티 관계도

```
Store (1) ──── (N) AdminUser
  │
  ├──── (N) Table
  │           │
  │           └──── (N) TableSession
  │                       │
  │                       └──── (N) Order [items 임베디드]
  │
  ├──── (N) Category
  │           │
  │           └──── (N) MenuItem
  │
  └──── Table ──── (N) OrderHistory
```

---

## 설계 변경 사항 (원본 대비)

| 원본 설계 | 변경 | 이유 |
|-----------|------|------|
| OrderItem 별도 테이블 | Order.items에 임베디드 | 항상 함께 조회, 단독 쿼리 불필요 |
| 9개 테이블 | 8개 테이블 | OrderItem 테이블 제거 (임베디드) |
