# Frontend Components Design

## 상태 관리 전략

| 영역 | 방식 | 이유 |
|------|------|------|
| 장바구니 | localStorage + React state | 페이지 새로고침 유지 필요 |
| 인증 토큰 | localStorage + Context | 전역 접근 필요 |
| 서버 데이터 | fetch + useState | 소규모 MVP, 별도 라이브러리 불필요 |
| SSE 이벤트 | EventSource + useState | 실시간 업데이트 |

---

## 고객용 컴포넌트 계층

### /customer (Layout)
```
CustomerLayout
├── Header (테이블 번호 표시, 네비게이션)
├── children (페이지 콘텐츠)
└── CartFloatingButton (장바구니 아이콘 + 수량 배지)
```

### /customer (메뉴 페이지 - 기본)
```
MenuPage
├── CategoryTabs (카테고리 필터 탭)
│   └── CategoryTab[] (각 카테고리 버튼)
├── MenuGrid
│   └── MenuCard[] (메뉴 카드)
│       ├── MenuInfo (이름, 가격, 설명)
│       └── AddToCartButton
└── MenuDetailModal (선택 시 상세 + 수량 선택)
```

**Props & State:**
- `MenuPage`: state: {categories, selectedCategory, menus, isLoading}
- `CategoryTabs`: props: {categories, selected, onSelect}
- `MenuCard`: props: {menu, onAddToCart}
- `MenuDetailModal`: props: {menu, isOpen, onClose, onAdd}

**API 연동:** `GET /api/menus?store_id={store_id}`

### /customer/cart (장바구니)
```
CartPage
├── CartItemList
│   └── CartItem[] (메뉴명, 가격, 수량 조절)
│       ├── ItemInfo
│       ├── QuantityControl (+/- 버튼)
│       └── RemoveButton
├── CartSummary (총 금액)
└── OrderButton (주문하기)
```

**Props & State:**
- `CartPage`: state: {cartItems} (localStorage에서 로드)
- `CartItem`: props: {item, onUpdateQty, onRemove}
- `CartSummary`: props: {totalAmount}

**API 연동:** 없음 (로컬 저장소만)

### /customer/orders (주문 내역)
```
OrdersPage
├── OrderList
│   └── OrderCard[] (주문 카드)
│       ├── OrderHeader (주문번호, 시각)
│       ├── StatusBadge (대기중/준비중/완료)
│       ├── OrderItems (메뉴 목록 축약)
│       └── OrderTotal (금액)
└── EmptyState (주문 없을 때)
```

**Props & State:**
- `OrdersPage`: state: {orders, isLoading}
- `OrderCard`: props: {order}
- `StatusBadge`: props: {status}

**API 연동:** `GET /api/orders?session_id={session_id}`

### 주문 성공 모달
```
OrderSuccessModal
├── SuccessIcon
├── OrderNumber
├── CountdownTimer (5초)
└── (자동 리다이렉트)
```

---

## 관리자용 컴포넌트 계층

### /admin/login
```
AdminLoginPage
├── LoginForm
│   ├── StoreIdInput
│   ├── UsernameInput
│   ├── PasswordInput
│   └── LoginButton
└── ErrorMessage
```

**Props & State:**
- `AdminLoginPage`: state: {storeId, username, password, error, isLoading}

**API 연동:** `POST /api/auth/admin/login`

### /admin (Layout)
```
AdminLayout
├── Sidebar (네비게이션)
│   ├── NavItem (대시보드)
│   ├── NavItem (테이블 관리)
│   └── NavItem (메뉴 관리)
├── Header (매장명, 로그아웃)
└── children (페이지 콘텐츠)
```

### /admin/dashboard (주문 모니터링)
```
DashboardPage
├── DashboardHeader (필터, 새로고침)
├── TableGrid
│   └── TableCard[] (테이블별 카드)
│       ├── TableHeader (번호, 총 금액)
│       ├── OrderPreviewList (최신 주문 미리보기)
│       │   └── OrderPreview[] (축약 정보)
│       └── ActionButtons (상태변경, 이용완료)
└── OrderDetailModal (카드 클릭 시)
    ├── FullOrderList
    └── StatusChangeButtons
```

**Props & State:**
- `DashboardPage`: state: {tables, orders, sseConnected}
- `TableCard`: props: {table, orders, onStatusChange, onComplete}
- `OrderDetailModal`: props: {table, orders, isOpen, onClose}

**API 연동:**
- `GET /api/sse/orders/{store_id}` (SSE 연결)
- `PATCH /api/orders/{order_id}/status`
- `POST /api/tables/{table_id}/complete`

### /admin/tables (테이블 관리)
```
TablesPage
├── TableSetupForm (새 테이블 추가)
│   ├── TableNumberInput
│   ├── PasswordInput
│   └── CreateButton
├── TableList
│   └── TableRow[] (테이블 행)
│       ├── TableInfo (번호, 상태, 총 금액)
│       ├── DeleteOrderButton
│       ├── CompleteButton
│       └── HistoryButton
└── HistoryModal (과거 내역)
    ├── DateFilter
    └── HistoryList
```

**API 연동:**
- `POST /api/tables`
- `GET /api/tables?store_id={store_id}`
- `DELETE /api/orders/{order_id}`
- `POST /api/tables/{table_id}/complete`
- `GET /api/tables/{table_id}/history`

### /admin/menus (메뉴 관리)
```
MenusPage
├── MenuForm (등록/수정 폼)
│   ├── NameInput
│   ├── PriceInput
│   ├── CategorySelect
│   ├── DescriptionInput
│   ├── SortOrderInput
│   └── SubmitButton
├── CategoryManager (카테고리 관리)
│   ├── CategoryForm
│   └── CategoryList
└── MenuList (등록된 메뉴)
    └── MenuItem[] (드래그 정렬 가능)
        ├── DragHandle
        ├── MenuInfo
        ├── EditButton
        └── DeleteButton
```

**API 연동:**
- `GET/POST/PUT/DELETE /api/menus`
- `GET/POST/PUT/DELETE /api/categories`

---

## 폼 검증 규칙 (클라이언트)

| 폼 | 필드 | 규칙 |
|----|------|------|
| 관리자 로그인 | storeId | 필수 |
| 관리자 로그인 | username | 필수 |
| 관리자 로그인 | password | 필수 |
| 메뉴 등록 | name | 필수, 1~50자 |
| 메뉴 등록 | price | 필수, 100~1,000,000 |
| 메뉴 등록 | category | 필수 |
| 테이블 설정 | table_number | 필수, 1~999 |
| 테이블 설정 | password | 필수, 4~20자 |

---

## SSE 연결 관리

```typescript
// SSE 연결 전략
1. 대시보드 마운트 시 EventSource 연결
2. 이벤트 수신 시 상태 업데이트
3. 연결 끊김 시 3초 후 자동 재연결 (최대 5회)
4. 대시보드 언마운트 시 연결 종료
5. 브라우저 탭 비활성 시에도 연결 유지
```

---

## 라우팅 및 인증 가드

| 라우트 | 인증 필요 | 가드 동작 |
|--------|:---------:|-----------|
| /customer/* | 테이블 토큰 | 토큰 없으면 초기 설정 화면 |
| /admin/login | 불필요 | 토큰 있으면 /admin/dashboard 리다이렉트 |
| /admin/* | 관리자 토큰 | 토큰 없으면 /admin/login 리다이렉트 |
