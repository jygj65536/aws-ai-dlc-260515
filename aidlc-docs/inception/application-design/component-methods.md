# 컴포넌트 메서드 정의 (Component Methods)

## 백엔드 API 엔드포인트

### BE-1: Auth

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| POST | `/api/auth/admin/login` | 관리자 로그인 | `{store_id, username, password}` | `{access_token, token_type}` |
| POST | `/api/auth/table/login` | 테이블 태블릿 로그인 | `{store_id, table_number, password}` | `{access_token, table_id, session_id}` |
| GET | `/api/auth/me` | 현재 인증 정보 확인 | Header: Bearer token | `{user_type, store_id, ...}` |

### BE-2: Store

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| GET | `/api/stores/{store_id}` | 매장 정보 조회 | path: store_id | `{store_id, name, ...}` |

### BE-3: Table

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| POST | `/api/tables` | 테이블 생성/초기 설정 | `{store_id, table_number, password}` | `{table_id, table_number}` |
| GET | `/api/tables` | 매장 테이블 목록 조회 | query: store_id | `[{table_id, table_number, session_status}]` |
| POST | `/api/tables/{table_id}/complete` | 이용 완료 처리 | path: table_id | `{success, message}` |
| GET | `/api/tables/{table_id}/history` | 과거 주문 내역 조회 | path: table_id, query: date_from, date_to | `[{session_id, orders, completed_at}]` |

### BE-4: Menu

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| GET | `/api/menus` | 메뉴 목록 조회 (카테고리 포함) | query: store_id | `{categories: [{id, name, items: [...]}]}` |
| POST | `/api/menus` | 메뉴 등록 | `{store_id, name, price, description, category_id, sort_order}` | `{menu_id, ...}` |
| PUT | `/api/menus/{menu_id}` | 메뉴 수정 | `{name, price, description, category_id, sort_order}` | `{menu_id, ...}` |
| DELETE | `/api/menus/{menu_id}` | 메뉴 삭제 | path: menu_id | `{success}` |
| GET | `/api/categories` | 카테고리 목록 조회 | query: store_id | `[{category_id, name, sort_order}]` |
| POST | `/api/categories` | 카테고리 등록 | `{store_id, name, sort_order}` | `{category_id, ...}` |
| PUT | `/api/categories/{category_id}` | 카테고리 수정 | `{name, sort_order}` | `{category_id, ...}` |
| DELETE | `/api/categories/{category_id}` | 카테고리 삭제 | path: category_id | `{success}` |

### BE-5: Order

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| POST | `/api/orders` | 주문 생성 | `{store_id, table_id, session_id, items: [{menu_id, name, quantity, price}]}` | `{order_id, order_number, total_amount}` |
| GET | `/api/orders` | 주문 목록 조회 | query: store_id, table_id, session_id | `[{order_id, order_number, status, items, total, created_at}]` |
| PATCH | `/api/orders/{order_id}/status` | 주문 상태 변경 | `{status: "preparing" \| "completed"}` | `{order_id, status}` |
| DELETE | `/api/orders/{order_id}` | 주문 삭제 (관리자) | path: order_id | `{success}` |

### BE-6: SSE

| Method | Endpoint | 설명 | Input | Output |
|--------|----------|------|-------|--------|
| GET | `/api/sse/orders/{store_id}` | 주문 실시간 스트림 | path: store_id | SSE stream (event: new_order, order_updated, order_deleted) |

---

## 프론트엔드 주요 페이지 인터페이스

### FE-1: Customer Menu Page
- `fetchMenus(storeId)` → 메뉴 목록 로드
- `filterByCategory(categoryId)` → 카테고리 필터
- `addToCart(menuItem, quantity)` → 장바구니 추가

### FE-2: Customer Cart
- `getCartItems()` → 로컬 저장소에서 장바구니 로드
- `updateQuantity(itemId, quantity)` → 수량 변경
- `removeItem(itemId)` → 항목 삭제
- `clearCart()` → 장바구니 비우기
- `calculateTotal()` → 총 금액 계산

### FE-3: Customer Order
- `submitOrder(cartItems)` → 주문 생성 API 호출
- `fetchOrderHistory(sessionId)` → 현재 세션 주문 내역 조회

### FE-4: Admin Login
- `login(storeId, username, password)` → 로그인 API 호출
- `storeToken(token)` → JWT 토큰 저장
- `checkSession()` → 세션 유효성 확인

### FE-5: Admin Dashboard
- `connectSSE(storeId)` → SSE 연결 수립
- `handleNewOrder(event)` → 신규 주문 처리
- `updateOrderStatus(orderId, status)` → 상태 변경
- `getTableSummary(storeId)` → 테이블별 요약 조회

### FE-6: Admin Table Management
- `setupTable(tableNumber, password)` → 테이블 초기 설정
- `deleteOrder(orderId)` → 주문 삭제
- `completeTable(tableId)` → 이용 완료 처리
- `fetchHistory(tableId, dateRange)` → 과거 내역 조회

### FE-7: Admin Menu Management
- `createMenu(menuData)` → 메뉴 등록
- `updateMenu(menuId, menuData)` → 메뉴 수정
- `deleteMenu(menuId)` → 메뉴 삭제
- `reorderMenus(menuIds)` → 순서 변경
