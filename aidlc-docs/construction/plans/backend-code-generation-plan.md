# Backend Code Generation Plan

## 유닛 정보
- **유닛명**: backend
- **기술**: FastAPI (Python 3.11+)
- **위치**: `backend/`
- **현재 범위**: Auth 기능 우선 구현 (US-9, US-5)

## 스토리 매핑
| Story ID | 스토리명 | 구현 내용 |
|----------|----------|-----------|
| US-9 | 매장 인증 | 관리자 로그인 API, JWT 발급 |
| US-5 | 테이블 자동 로그인/세션 | 테이블 로그인 API, JWT 발급 |

## 의존성
- DynamoDB 테이블: Store, AdminUser, Table, TableSession
- 외부 패키지: fastapi, uvicorn, boto3, python-jose, passlib[bcrypt], pydantic

---

## 실행 계획

### Step 1: 프로젝트 구조 초기화
- [x] `backend/` 디렉토리 생성
- [x] `backend/requirements.txt` 생성 (의존성 목록)
- [x] `backend/.env.example` 생성 (환경변수 템플릿)
- [x] `backend/app/__init__.py` 생성
- [x] `backend/app/main.py` 생성 (FastAPI 앱 진입점, CORS 설정)
- [x] `backend/app/config.py` 생성 (환경변수 로드, 설정 클래스)

### Step 2: Core 레이어 구현
- [x] `backend/app/core/__init__.py` 생성
- [x] `backend/app/core/dynamodb.py` 생성 (DynamoDB 클라이언트 초기화)
- [x] `backend/app/core/security.py` 생성 (JWT 생성/검증, bcrypt 유틸)

### Step 3: Auth 모델 (Pydantic 스키마)
- [x] `backend/app/models/__init__.py` 생성
- [x] `backend/app/models/auth.py` 생성 (요청/응답 스키마: AdminLoginRequest, TableLoginRequest, TokenResponse, CurrentUser)

### Step 4: Auth Repository 레이어
- [x] `backend/app/repositories/__init__.py` 생성
- [x] `backend/app/repositories/admin_user_repository.py` 생성 (AdminUser CRUD: get_by_username, update_login_attempts, lock_account, reset_attempts)
- [x] `backend/app/repositories/table_repository.py` 생성 (Table 조회: get_by_table_number)
- [x] `backend/app/repositories/session_repository.py` 생성 (TableSession 조회: get_active_session)

### Step 5: Auth Service 레이어 (비즈니스 로직)
- [x] `backend/app/services/__init__.py` 생성
- [x] `backend/app/services/auth_service.py` 생성
  - `admin_login(store_id, username, password)` — AUTH-01, AUTH-02 규칙 적용
  - `table_login(store_id, table_number, password)` — AUTH-03 규칙 적용
  - `get_current_user(token)` — JWT 검증 및 사용자 컨텍스트 반환

### Step 6: 의존성 주입 (Dependencies)
- [x] `backend/app/dependencies.py` 생성 (get_current_user, require_admin, require_table, require_store_match)

### Step 7: Auth Router (API 엔드포인트)
- [x] `backend/app/routers/__init__.py` 생성
- [x] `backend/app/routers/auth.py` 생성
  - `POST /api/auth/admin/login` — 관리자 로그인
  - `POST /api/auth/table/login` — 테이블 로그인
  - `GET /api/auth/me` — 현재 인증 정보 확인

### Step 8: DynamoDB 테이블 생성 스크립트
- [x] `backend/scripts/create_tables.py` 생성 (Store, AdminUser, Table, TableSession 테이블 + GSI 생성)
- [x] `backend/scripts/seed_data.py` 생성 (테스트용 초기 데이터: 매장 1개, 관리자 1명, 테이블 2개)

### Step 9: Auth 단위 테스트
- [x] `backend/tests/__init__.py` 생성
- [x] `backend/tests/conftest.py` 생성 (pytest fixtures, mock DynamoDB)
- [x] `backend/tests/test_auth_service.py` 생성 (auth_service 단위 테스트)
- [x] `backend/tests/test_auth_router.py` 생성 (auth router 통합 테스트)

### Step 10: 문서 및 요약
- [x] `aidlc-docs/construction/backend/code/auth-summary.md` 생성 (구현 요약)
- [x] `backend/README.md` 생성 (실행 방법, 환경 설정 가이드)

---

## 비즈니스 규칙 적용 매핑

| 규칙 ID | 규칙 | 적용 위치 |
|---------|------|-----------|
| AUTH-01 | 관리자 로그인 시도 제한 (5회/15분) | auth_service.py - admin_login() |
| AUTH-02 | 관리자 JWT 16시간 만료 | security.py - create_access_token() |
| AUTH-03 | 테이블 JWT 16시간 만료 | security.py - create_access_token() |
| AUTH-04 | 관리자 전용 API 보호 | dependencies.py - require_admin() |
| AUTH-05 | 테이블 전용 API 보호 | dependencies.py - require_table() |
| AUTH-06 | 매장 격리 | dependencies.py - require_store_match() |

## 총 스텝 수: 10
## 예상 파일 수: ~25개
