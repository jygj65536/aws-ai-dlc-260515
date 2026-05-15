# 컴포넌트 의존성 (Component Dependencies)

## 의존성 매트릭스 (백엔드)

| 컴포넌트 | AuthService | StoreService | TableService | MenuService | OrderService | SSEManager |
|----------|:-----------:|:------------:|:------------:|:-----------:|:------------:|:----------:|
| **AuthService** | - | - | R | - | - | - |
| **StoreService** | - | - | - | - | - | - |
| **TableService** | - | - | - | - | R | W |
| **MenuService** | - | - | - | - | - | - |
| **OrderService** | - | - | R | - | - | W |
| **SSEManager** | - | - | - | - | - | - |

- **R**: Read 의존 (데이터 조회)
- **W**: Write 의존 (이벤트 발행/상태 변경)

---

## 의존성 방향

```
+------------------+     +------------------+
|   AuthService    |---->|  TableRepository |
+------------------+     +------------------+
                         |  AdminRepository |
                         +------------------+

+------------------+     +------------------+     +------------------+
|  OrderService    |---->| OrderRepository  |     |   SSEManager     |
+------------------+     +------------------+     +------------------+
        |                                                  ^
        |                                                  |
        +--------------------------------------------------+
        |
        v
+------------------+
|  TableService    |---->  SessionRepository, OrderHistoryRepository
+------------------+
        |
        +---> SSEManager (이용 완료 이벤트)

+------------------+     +------------------+
|   MenuService    |---->| MenuRepository   |
+------------------+     | CategoryRepo     |
                         +------------------+
```

---

## 프론트엔드 → 백엔드 의존성

| 프론트엔드 컴포넌트 | 백엔드 API 의존 |
|---------------------|-----------------|
| Customer Menu | `GET /api/menus` |
| Customer Cart | 로컬 저장소만 (API 의존 없음) |
| Customer Order | `POST /api/orders`, `GET /api/orders` |
| Admin Login | `POST /api/auth/admin/login` |
| Admin Dashboard | `GET /api/sse/orders/{store_id}`, `PATCH /api/orders/{id}/status` |
| Admin Tables | `POST /api/tables`, `POST /api/tables/{id}/complete`, `DELETE /api/orders/{id}`, `GET /api/tables/{id}/history` |
| Admin Menus | `GET/POST/PUT/DELETE /api/menus`, `GET/POST/PUT/DELETE /api/categories` |

---

## 데이터 흐름

### 고객 주문 흐름
```
[태블릿] → 메뉴 조회 → [백엔드 Menu API]
[태블릿] → 장바구니 (로컬) → 주문 확정 → [백엔드 Order API]
[백엔드 Order API] → SSE 이벤트 → [관리자 대시보드]
```

### 관리자 모니터링 흐름
```
[관리자 브라우저] ← SSE 스트림 ← [백엔드 SSE Manager]
[관리자 브라우저] → 상태 변경 → [백엔드 Order API]
[관리자 브라우저] → 이용 완료 → [백엔드 Table API]
```

---

## DynamoDB 테이블 의존성

| DynamoDB 테이블 | 접근하는 서비스 |
|----------------|----------------|
| Store | StoreService, AuthService |
| AdminUser | AuthService |
| Table | AuthService, TableService |
| TableSession | TableService, OrderService |
| Category | MenuService |
| MenuItem | MenuService |
| Order | OrderService, TableService |
| OrderItem | OrderService |
| OrderHistory | TableService |
