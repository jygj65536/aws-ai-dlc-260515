# Unit of Work 정의

## 분해 전략
- **접근 방식**: 레이어 기반 (백엔드 + 프론트엔드)
- **개발 순서**: 순차 (백엔드 먼저 → 프론트엔드)
- **근거**: 모노레포 + 소규모 MVP + 1인 개발 환경에 최적

---

## Unit 1: Backend (FastAPI)

| 항목 | 내용 |
|------|------|
| **유닛명** | backend |
| **기술** | FastAPI (Python 3.11+) |
| **위치** | `backend/` |
| **책임** | REST API, 비즈니스 로직, DynamoDB 접근, SSE 관리 |
| **배포** | 로컬 서버 (uvicorn) |

### 포함 컴포넌트
- BE-1: Auth (Router/Service/Repository)
- BE-2: Store (Router/Service/Repository)
- BE-3: Table (Router/Service/Repository)
- BE-4: Menu (Router/Service/Repository)
- BE-5: Order (Router/Service/Repository)
- BE-6: SSE Manager

### 디렉토리 구조
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── config.py               # 설정 (환경변수, DynamoDB 설정)
│   ├── dependencies.py         # 의존성 주입 (인증 등)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── stores.py
│   │   ├── tables.py
│   │   ├── menus.py
│   │   ├── orders.py
│   │   └── sse.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── store_service.py
│   │   ├── table_service.py
│   │   ├── menu_service.py
│   │   ├── order_service.py
│   │   └── sse_manager.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── admin_user_repository.py
│   │   ├── store_repository.py
│   │   ├── table_repository.py
│   │   ├── session_repository.py
│   │   ├── menu_repository.py
│   │   ├── category_repository.py
│   │   ├── order_repository.py
│   │   └── order_history_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py             # 요청/응답 스키마
│   │   ├── store.py
│   │   ├── table.py
│   │   ├── menu.py
│   │   └── order.py
│   └── core/
│       ├── __init__.py
│       ├── security.py         # JWT, bcrypt 유틸
│       └── dynamodb.py         # DynamoDB 클라이언트
├── requirements.txt
├── .env.example
└── README.md
```

### 주요 의존성 (Python 패키지)
- fastapi
- uvicorn
- boto3 (DynamoDB)
- python-jose (JWT)
- passlib[bcrypt] (비밀번호 해싱)
- pydantic (데이터 검증)
- sse-starlette (SSE 지원)

---

## Unit 2: Frontend (Next.js)

| 항목 | 내용 |
|------|------|
| **유닛명** | frontend |
| **기술** | Next.js 14+ (TypeScript, App Router) |
| **위치** | `frontend/` |
| **책임** | 고객용 UI, 관리자 UI, API 통신, 로컬 상태 관리 |
| **배포** | 로컬 서버 (next start) |

### 포함 컴포넌트
- FE-1: Customer Menu Page
- FE-2: Customer Cart
- FE-3: Customer Order
- FE-4: Admin Login
- FE-5: Admin Dashboard
- FE-6: Admin Table Management
- FE-7: Admin Menu Management
- FE-8: Shared Components

### 디렉토리 구조
```
frontend/
├── app/
│   ├── layout.tsx              # 루트 레이아웃
│   ├── page.tsx                # 랜딩 (리다이렉트)
│   ├── customer/
│   │   ├── layout.tsx          # 고객 레이아웃
│   │   ├── page.tsx            # 메뉴 화면 (기본)
│   │   ├── cart/
│   │   │   └── page.tsx        # 장바구니
│   │   └── orders/
│   │       └── page.tsx        # 주문 내역
│   └── admin/
│       ├── layout.tsx          # 관리자 레이아웃
│       ├── login/
│       │   └── page.tsx        # 로그인
│       ├── dashboard/
│       │   └── page.tsx        # 주문 모니터링
│       ├── tables/
│       │   └── page.tsx        # 테이블 관리
│       └── menus/
│           └── page.tsx        # 메뉴 관리
├── components/
│   ├── ui/                     # 공통 UI (Button, Card, Modal 등)
│   ├── customer/               # 고객 전용 컴포넌트
│   └── admin/                  # 관리자 전용 컴포넌트
├── lib/
│   ├── api.ts                  # API 클라이언트
│   ├── auth.ts                 # 인증 유틸
│   ├── cart.ts                 # 장바구니 로컬 저장
│   └── sse.ts                  # SSE 연결 유틸
├── types/
│   └── index.ts                # TypeScript 타입 정의
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.ts
```

### 주요 의존성 (npm 패키지)
- next
- react, react-dom
- typescript
- tailwindcss (스타일링)
- zustand 또는 Context API (상태 관리)

---

## 개발 순서

```
Phase 1: Backend (Unit 1)
  → API 전체 구현 + DynamoDB 테이블 생성 + SSE 구현

Phase 2: Frontend (Unit 2)
  → 백엔드 API 연동 + UI 구현 + SSE 클라이언트
```
