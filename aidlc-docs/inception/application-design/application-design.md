# 테이블오더 서비스 - Application Design (통합 문서)

## 1. 아키텍처 개요

### 기술 스택
| 영역 | 기술 | 역할 |
|------|------|------|
| 백엔드 | FastAPI (Python) | REST API + SSE 서버 |
| 프론트엔드 | Next.js (TypeScript) | 고객용 + 관리자용 웹앱 |
| 데이터베이스 | DynamoDB | NoSQL 데이터 저장 |
| 실시간 통신 | SSE (Server-Sent Events) | 주문 모니터링 |

### 설계 결정사항
| 결정 | 선택 | 근거 |
|------|------|------|
| 백엔드 구조 | 레이어드 아키텍처 (Router→Service→Repository) | 관심사 분리, 테스트 용이 |
| 프론트엔드 구조 | 단일 Next.js 앱 (라우팅 분리) | 소규모 MVP에 적합, 코드 공유 |
| DB 설계 | Table-per-Entity | 직관적, DynamoDB 학습 곡선 완화 |
| 통신 | REST + SSE | 요구사항 충족, WebSocket 대비 단순 |
| 프로젝트 구조 | 모노레포 (backend/ + frontend/) | 단일 팀 관리 편의 |

---

## 2. 시스템 아키텍처

```
+-------------------+          +-------------------+
|   Customer        |   REST   |                   |
|   (Tablet)        |--------->|                   |
|   Next.js         |          |   FastAPI         |
+-------------------+          |   Backend         |       +-----------+
                               |                   |------>| DynamoDB  |
+-------------------+   REST   |   - Routers       |       | (9 Tables)|
|   Admin           |--------->|   - Services      |       +-----------+
|   (Browser)       |<---------|   - Repositories  |
|   Next.js         |   SSE    |   - SSE Manager   |
+-------------------+          +-------------------+
```

---

## 3. 백엔드 컴포넌트 (6개)

| ID | 컴포넌트 | 책임 |
|----|----------|------|
| BE-1 | Auth | 관리자/테이블 인증, JWT 토큰 관리 |
| BE-2 | Store | 매장 정보 관리 |
| BE-3 | Table | 테이블 CRUD, 세션 관리, 이용 완료 |
| BE-4 | Menu | 메뉴/카테고리 CRUD, 순서 관리 |
| BE-5 | Order | 주문 CRUD, 상태 관리, SSE 이벤트 발행 |
| BE-6 | SSE Manager | SSE 연결 풀, 매장별 브로드캐스트 |

---

## 4. 프론트엔드 컴포넌트 (8개)

| ID | 컴포넌트 | 라우트 | 책임 |
|----|----------|--------|------|
| FE-1 | Customer Menu | `/customer` | 메뉴 조회, 카테고리 필터 |
| FE-2 | Customer Cart | `/customer/cart` | 장바구니 관리 (로컬) |
| FE-3 | Customer Order | `/customer/orders` | 주문 생성, 내역 조회 |
| FE-4 | Admin Login | `/admin/login` | 관리자 인증 |
| FE-5 | Admin Dashboard | `/admin/dashboard` | 실시간 주문 모니터링 (SSE) |
| FE-6 | Admin Tables | `/admin/tables` | 테이블 관리 |
| FE-7 | Admin Menus | `/admin/menus` | 메뉴 관리 |
| FE-8 | Shared | `components/`, `lib/` | 공통 UI, API 클라이언트 |

---

## 5. API 엔드포인트 요약 (17개)

| 도메인 | 엔드포인트 수 | 주요 기능 |
|--------|:---:|------|
| Auth | 3 | 로그인(관리자/테이블), 인증 확인 |
| Store | 1 | 매장 정보 조회 |
| Table | 4 | CRUD, 이용 완료, 과거 내역 |
| Menu | 8 | 메뉴/카테고리 CRUD |
| Order | 4 | 주문 CRUD, 상태 변경 |
| SSE | 1 | 실시간 스트림 |

---

## 6. DynamoDB 테이블 (9개)

| 테이블명 | PK | SK | 용도 |
|----------|----|----|------|
| Store | store_id | - | 매장 정보 |
| AdminUser | store_id | username | 관리자 계정 |
| Table | store_id | table_id | 테이블 정보 |
| TableSession | table_id | session_id | 테이블 세션 |
| Category | store_id | category_id | 메뉴 카테고리 |
| MenuItem | store_id | menu_id | 메뉴 항목 |
| Order | session_id | order_id | 주문 |
| OrderItem | order_id | item_id | 주문 항목 |
| OrderHistory | table_id | history_id | 과거 주문 이력 |

---

## 7. 핵심 플로우

### 주문 생성
고객 장바구니 → POST /api/orders → OrderService → DynamoDB 저장 → SSE 브로드캐스트 → 관리자 대시보드 표시

### 이용 완료
관리자 클릭 → POST /api/tables/{id}/complete → TableService → 주문 이력 이동 → 세션 종료 → 테이블 리셋 → SSE 브로드캐스트

---

## 상세 문서 참조
- 컴포넌트 상세: `components.md`
- 메서드 시그니처: `component-methods.md`
- 서비스 설계: `services.md`
- 의존성 관계: `component-dependency.md`
