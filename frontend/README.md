# 테이블오더 프론트엔드

Next.js 14 기반 테이블오더 서비스 프론트엔드 (고객용 + 관리자용)

## 기술 스택

- **프레임워크**: Next.js 14 (App Router)
- **언어**: TypeScript
- **스타일링**: Tailwind CSS
- **상태 관리**: React Context + useState + localStorage
- **실시간 통신**: EventSource (SSE)
- **브라우저 지원**: Chrome, Firefox, Safari (최신 2개 버전)

## 설치 및 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행 (http://localhost:3000)
npm run dev

# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

## 프로젝트 구조

```
frontend/
├── app/                    # Next.js App Router 페이지
│   ├── layout.tsx          # 루트 레이아웃
│   ├── page.tsx            # 랜딩 (→ /customer 리다이렉트)
│   ├── customer/           # 고객용 페이지
│   │   ├── layout.tsx      # 고객 레이아웃 + 인증 가드
│   │   ├── page.tsx        # 메뉴 화면 (기본)
│   │   ├── cart/page.tsx   # 장바구니
│   │   ├── orders/page.tsx # 주문 내역
│   │   └── setup/page.tsx  # 초기 설정
│   └── admin/              # 관리자용 페이지
│       ├── layout.tsx      # 관리자 레이아웃 + 인증 가드
│       ├── login/page.tsx  # 로그인
│       ├── dashboard/page.tsx # 주문 모니터링
│       ├── tables/page.tsx # 테이블 관리
│       └── menus/page.tsx  # 메뉴 관리
├── components/             # 재사용 컴포넌트
│   ├── ui/                 # 공통 UI (Button, Card, Modal 등)
│   ├── customer/           # 고객 전용 컴포넌트
│   └── admin/              # 관리자 전용 컴포넌트
├── lib/                    # 유틸리티
│   ├── api.ts              # API 클라이언트
│   ├── auth.ts             # 인증 유틸
│   ├── cart.ts             # 장바구니 로컬 저장
│   └── sse.ts              # SSE 연결 유틸
└── types/                  # TypeScript 타입 정의
    └── index.ts
```

## API 연동

백엔드 API 서버(FastAPI)가 `http://localhost:8000`에서 실행 중이어야 합니다.
`next.config.js`에서 `/api/*` 요청을 백엔드로 프록시합니다.

## 주요 기능

### 고객용 (/customer)
- 메뉴 조회 및 카테고리 필터링
- 장바구니 관리 (localStorage 기반)
- 주문 생성 및 주문 내역 조회
- 태블릿 자동 로그인

### 관리자용 (/admin)
- 매장 인증 (JWT)
- 실시간 주문 모니터링 (SSE)
- 테이블 관리 (생성, 이용 완료, 과거 내역)
- 메뉴/카테고리 CRUD
