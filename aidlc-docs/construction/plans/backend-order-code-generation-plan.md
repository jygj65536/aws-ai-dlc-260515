# Code Generation Plan - Backend Order Feature

## 유닛 컨텍스트
- **유닛**: Backend (FastAPI)
- **브랜치**: feature/order
- **범위**: 주문(Order) 관련 기능만 구현
- **관련 스토리**: US-3 (주문 생성), US-4 (주문 내역 조회), US-6 (실시간 주문 모니터링)
- **의존성**: DynamoDB 클라이언트, 설정, 공통 모델 기반

## 다른 브랜치에서 구현 예정 (이 브랜치에서 제외)
- Auth (US-9, US-5): feature/auth 브랜치
- Menu (US-1, US-8): feature/menu 브랜치
- Table 관리 (US-7): feature/table 브랜치

## 이 브랜치에서 구현할 내용
Order 도메인 + 필요한 공통 인프라 (다른 브랜치에서도 사용할 기반 코드)

---

## Code Generation Steps

### Step 1: 프로젝트 구조 및 공통 인프라 설정
- [x] `backend/app/__init__.py` 생성
- [x] `backend/app/main.py` - FastAPI 앱 진입점 (Order 라우터만 등록)
- [x] `backend/app/config.py` - 환경변수 설정 (DynamoDB endpoint, region 등)
- [x] `backend/app/core/__init__.py` 생성
- [x] `backend/app/core/dynamodb.py` - DynamoDB 클라이언트 초기화
- [x] `backend/requirements.txt` - Python 의존성 패키지
- [x] `backend/.env.example` - 환경변수 예시

### Step 2: Order 도메인 모델 (Pydantic 스키마)
- [x] `backend/app/models/__init__.py` 생성
- [x] `backend/app/models/order.py` - 주문 요청/응답 스키마 정의
  - CreateOrderRequest (items, store_id, table_id, session_id)
  - OrderItem (menu_id, name, quantity, price)
  - CreateOrderResponse (order_id, order_number, total_amount, session_id)
  - UpdateOrderStatusRequest (status)
  - OrderResponse (전체 주문 정보)
  - OrderListResponse

### Step 3: Order Repository 레이어
- [x] `backend/app/repositories/__init__.py` 생성
- [x] `backend/app/repositories/order_repository.py` - DynamoDB Order 테이블 접근
  - save(order) - 주문 저장
  - get_by_id(session_id, order_id) - 주문 단건 조회
  - get_by_session(session_id) - 세션별 주문 목록
  - get_by_store(store_id) - 매장별 주문 목록 (GSI)
  - update_status(session_id, order_id, status) - 상태 업데이트
  - delete(session_id, order_id) - 주문 삭제
  - get_next_order_number(store_id) - 매장별 순번 조회
- [x] `backend/app/repositories/session_repository.py` - TableSession 접근
  - get_by_id(table_id, session_id) - 세션 조회
  - create(session) - 세션 생성
  - update_total_amount(table_id, session_id, amount) - 총액 업데이트
  - update_status(table_id, session_id, status) - 상태 업데이트
- [x] `backend/app/repositories/table_repository.py` - Table 접근 (세션 연결용)
  - get_by_id(store_id, table_id) - 테이블 조회
  - update_session_id(store_id, table_id, session_id) - 현재 세션 업데이트
- [x] `backend/app/repositories/order_history_repository.py` - OrderHistory 접근
  - save(history) - 이력 저장
  - get_by_table(table_id, date_from, date_to) - 테이블별 이력 조회

### Step 4: SSE Manager
- [x] `backend/app/services/__init__.py` 생성
- [x] `backend/app/services/sse_manager.py` - SSE 연결 관리
  - connect(store_id) - 연결 등록, EventSourceResponse 반환
  - disconnect(store_id, queue) - 연결 해제
  - broadcast(store_id, event_type, data) - 이벤트 브로드캐스트

### Step 5: Order Service 레이어
- [x] `backend/app/services/order_service.py` - 주문 비즈니스 로직
  - create_order(order_data) - 주문 생성 (세션 처리 포함)
  - get_orders(store_id, session_id) - 주문 목록 조회
  - update_order_status(order_id, session_id, new_status) - 상태 변경
  - delete_order(order_id, session_id) - 주문 삭제
  - _ensure_active_session(store_id, table_id, session_id) - 세션 활성화 확인
  - _validate_status_transition(current, new) - 상태 전이 검증

### Step 6: Order Router (API 엔드포인트)
- [x] `backend/app/routers/__init__.py` 생성
- [x] `backend/app/routers/orders.py` - 주문 API 엔드포인트
  - POST /api/orders - 주문 생성
  - GET /api/orders - 주문 목록 조회 (query: store_id, session_id)
  - PATCH /api/orders/{order_id}/status - 상태 변경
  - DELETE /api/orders/{order_id} - 주문 삭제
- [x] `backend/app/routers/sse.py` - SSE 스트림 엔드포인트
  - GET /api/sse/orders/{store_id} - 실시간 주문 스트림

### Step 7: 의존성 주입 및 인증 스텁
- [x] `backend/app/dependencies.py` - 의존성 주입
  - get_db() - DynamoDB 리소스
  - get_current_user() - 인증 스텁 (다른 브랜치에서 실제 구현)
  - get_order_service() - OrderService 인스턴스
  - get_sse_manager() - SSEManager 싱글톤

### Step 8: DynamoDB 테이블 생성 스크립트
- [x] `backend/scripts/create_tables.py` - 로컬 DynamoDB 테이블 생성
  - Order 테이블 (PK: session_id, SK: order_id, GSI: StoreOrderIndex)
  - TableSession 테이블 (PK: table_id, SK: session_id)
  - Table 테이블 (PK: store_id, SK: table_id, GSI: TableNumberIndex)
  - OrderHistory 테이블 (PK: table_id, SK: history_id, GSI: DateIndex)

### Step 9: 문서 생성
- [x] `backend/README.md` - 백엔드 실행 가이드
- [x] `aidlc-docs/construction/backend/code/order-code-summary.md` - 코드 요약 문서

---

## 스토리 트레이서빌리티

| Step | 관련 스토리 | 구현 내용 |
|------|------------|-----------|
| Step 1 | 공통 | 프로젝트 기반 인프라 |
| Step 2 | US-3, US-4 | 주문 데이터 모델 |
| Step 3 | US-3, US-4, US-6 | 데이터 접근 레이어 |
| Step 4 | US-6 | 실시간 이벤트 관리 |
| Step 5 | US-3, US-4, US-6 | 비즈니스 로직 |
| Step 6 | US-3, US-4, US-6 | API 엔드포인트 |
| Step 7 | 공통 | 의존성 주입 |
| Step 8 | 공통 | DB 테이블 생성 |
| Step 9 | 공통 | 문서화 |

---

## 기술 결정 사항
- **Python 버전**: 3.11+ (venv 이미 3.12로 생성됨)
- **DynamoDB**: boto3 + 로컬 DynamoDB (docker)
- **SSE**: sse-starlette 라이브러리
- **인증**: 스텁으로 구현 (feature/auth 브랜치에서 실제 구현)
- **검증**: Pydantic v2
- **비동기**: FastAPI async/await 패턴
