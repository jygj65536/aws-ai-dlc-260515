# Code Generation Plan - Frontend (Unit 2)

## 유닛 개요

| 항목 | 내용 |
|------|------|
| **유닛명** | frontend |
| **기술** | Next.js 14+ (TypeScript, App Router) |
| **위치** | `frontend/` |
| **책임** | 고객용 UI, 관리자 UI, API 통신, 로컬 상태 관리 |
| **의존성** | Backend API (Unit 1) |

## 구현 스토리 매핑

| 스토리 | 구현 범위 |
|--------|-----------|
| US-1 | 메뉴 조회 및 탐색 (고객 메뉴 페이지) |
| US-2 | 장바구니 관리 (장바구니 페이지) |
| US-3 | 주문 생성 (주문 확정 플로우) |
| US-4 | 주문 내역 조회 (주문 내역 페이지) |
| US-5 | 테이블 자동 로그인 및 세션 관리 (인증 가드) |
| US-6 | 실시간 주문 모니터링 (관리자 대시보드) |
| US-7 | 테이블 관리 (관리자 테이블 페이지) |
| US-8 | 메뉴 관리 (관리자 메뉴 페이지) |
| US-9 | 매장 인증 (관리자 로그인) |

---

## 실행 계획

### Step 1: 프로젝트 구조 및 설정 파일 생성
- [x] `frontend/package.json` (의존성 정의)
- [x] `frontend/tsconfig.json` (TypeScript 설정)
- [x] `frontend/next.config.js` (Next.js 설정, API 프록시)
- [x] `frontend/tailwind.config.ts` (Tailwind CSS 설정)
- [x] `frontend/postcss.config.js`
- [x] `frontend/app/globals.css` (글로벌 스타일)

### Step 2: TypeScript 타입 정의
- [x] `frontend/types/index.ts` (모든 도메인 타입: Store, Table, Session, Category, MenuItem, Order, OrderItem, Auth 관련)

### Step 3: 공통 유틸리티 라이브러리
- [x] `frontend/lib/api.ts` (API 클라이언트 - fetch 래퍼, 인증 헤더, 에러 처리)
- [x] `frontend/lib/auth.ts` (인증 유틸 - 토큰 저장/조회/삭제, 만료 체크)
- [x] `frontend/lib/cart.ts` (장바구니 로컬 저장소 관리)
- [x] `frontend/lib/sse.ts` (SSE 연결 유틸 - 연결/재연결/종료)

### Step 4: 공통 UI 컴포넌트
- [x] `frontend/components/ui/Button.tsx`
- [x] `frontend/components/ui/Card.tsx`
- [x] `frontend/components/ui/Modal.tsx`
- [x] `frontend/components/ui/Input.tsx`
- [x] `frontend/components/ui/Badge.tsx`
- [x] `frontend/components/ui/LoadingSpinner.tsx`
- [x] `frontend/components/ui/ErrorMessage.tsx`
- [x] `frontend/components/ui/ConfirmDialog.tsx`

### Step 5: 루트 레이아웃 및 랜딩 페이지
- [x] `frontend/app/layout.tsx` (루트 레이아웃)
- [x] `frontend/app/page.tsx` (랜딩 - /customer로 리다이렉트)

### Step 6: 고객용 레이아웃 및 인증 (US-5)
- [x] `frontend/app/customer/layout.tsx` (고객 레이아웃 + 인증 가드)
- [x] `frontend/components/customer/CustomerHeader.tsx`
- [x] `frontend/components/customer/CartFloatingButton.tsx`
- [x] `frontend/app/customer/setup/page.tsx` (초기 설정 페이지 - 토큰 없을 때)

### Step 7: 고객 메뉴 페이지 (US-1)
- [x] `frontend/app/customer/page.tsx` (메뉴 페이지 - 기본 화면)
- [x] `frontend/components/customer/CategoryTabs.tsx`
- [x] `frontend/components/customer/MenuGrid.tsx`
- [x] `frontend/components/customer/MenuCard.tsx`
- [x] `frontend/components/customer/MenuDetailModal.tsx`

### Step 8: 고객 장바구니 페이지 (US-2)
- [x] `frontend/app/customer/cart/page.tsx`
- [x] `frontend/components/customer/CartItemList.tsx`
- [x] `frontend/components/customer/CartItem.tsx`
- [x] `frontend/components/customer/CartSummary.tsx`

### Step 9: 고객 주문 생성 및 내역 (US-3, US-4)
- [x] `frontend/app/customer/orders/page.tsx` (주문 내역)
- [x] `frontend/components/customer/OrderCard.tsx`
- [x] `frontend/components/customer/StatusBadge.tsx`
- [x] `frontend/components/customer/OrderSuccessModal.tsx`

### Step 10: 관리자 로그인 (US-9)
- [x] `frontend/app/admin/login/page.tsx`
- [x] `frontend/components/admin/LoginForm.tsx`

### Step 11: 관리자 레이아웃 및 인증 가드
- [x] `frontend/app/admin/layout.tsx` (관리자 레이아웃 + 인증 가드)
- [x] `frontend/components/admin/AdminSidebar.tsx`
- [x] `frontend/components/admin/AdminHeader.tsx`

### Step 12: 관리자 대시보드 (US-6)
- [x] `frontend/app/admin/dashboard/page.tsx`
- [x] `frontend/components/admin/TableGrid.tsx`
- [x] `frontend/components/admin/TableCard.tsx`
- [x] `frontend/components/admin/OrderDetailModal.tsx`

### Step 13: 관리자 테이블 관리 (US-7)
- [x] `frontend/app/admin/tables/page.tsx`
- [x] `frontend/components/admin/TableSetupForm.tsx`
- [x] `frontend/components/admin/TableList.tsx`
- [x] `frontend/components/admin/TableRow.tsx`
- [x] `frontend/components/admin/HistoryModal.tsx`

### Step 14: 관리자 메뉴 관리 (US-8)
- [x] `frontend/app/admin/menus/page.tsx`
- [x] `frontend/components/admin/MenuForm.tsx`
- [x] `frontend/components/admin/CategoryManager.tsx`
- [x] `frontend/components/admin/MenuList.tsx`
- [x] `frontend/components/admin/MenuItemRow.tsx`

### Step 15: README 및 문서
- [x] `frontend/README.md` (설치, 실행, 구조 설명)
- [x] `aidlc-docs/construction/frontend/code/code-generation-summary.md` (코드 생성 요약)

---

## 기술 결정사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 상태 관리 | React Context + useState | 소규모 MVP, 외부 라이브러리 불필요 |
| 스타일링 | Tailwind CSS | 빠른 개발, 일관된 디자인 (Next.js 기본 지원) |
| API 통신 | fetch API (네이티브) | 브라우저 내장, 별도 라이브러리 불필요 |
| 폼 검증 | 클라이언트 직접 구현 | 간단한 규칙, 라이브러리 불필요 |
| SSE | EventSource API (네이티브) | 브라우저 내장 API |
| 장바구니 | localStorage + React state | 새로고침 유지 필요 |
| 드래그 정렬 | HTML Drag and Drop API (네이티브) | 외부 라이브러리 없이 구현 |

## 의존성 정책 (최소화)

**런타임 의존성 (npm packages)**:
- `next` / `react` / `react-dom` — 프레임워크 필수
- `typescript` — 타입 안전성 (devDependency)
- `tailwindcss` / `postcss` / `autoprefixer` — 스타일링 (devDependency)
- `@types/react` / `@types/node` — 타입 정의 (devDependency)

**사용하지 않는 것들** (의존성 최소화):
- ❌ axios, swr, react-query (fetch API로 대체)
- ❌ zustand, redux, jotai (Context API로 대체)
- ❌ react-hook-form, formik (직접 구현)
- ❌ dnd-kit, react-beautiful-dnd (네이티브 Drag API)
- ❌ date-fns, dayjs (Intl API로 대체)

## 브라우저 호환성

| 브라우저 | 최소 버전 | 비고 |
|----------|-----------|------|
| Chrome | 최신 2개 버전 | 주요 타겟 |
| Firefox | 최신 2개 버전 | 지원 |
| Safari | 최신 2개 버전 | 지원 |

**호환성 전략**:
- ES2020+ 문법 사용 (모든 타겟 브라우저 지원)
- EventSource API: Chrome/Firefox/Safari 모두 네이티브 지원
- localStorage: 모든 타겟 브라우저 지원
- CSS: Tailwind CSS가 autoprefixer로 벤더 프리픽스 자동 처리

## 자동화 친화적 코드 규칙
- 모든 인터랙티브 요소에 `data-testid` 속성 추가
- 네이밍 규칙: `{component}-{element-role}` (예: `menu-card-add-button`)
- 동적 ID 사용 금지, 안정적인 testid 유지

