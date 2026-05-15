# Unit of Work 의존성

## 유닛 간 의존성 매트릭스

| 유닛 | Backend | Frontend |
|------|:-------:|:--------:|
| **Backend** | - | - |
| **Frontend** | ✅ 의존 | - |

- Frontend → Backend: REST API + SSE 연결 의존
- Backend: 독립적 (외부 의존 없음, DynamoDB만 필요)

---

## 개발 순서 및 통합 전략

### 순서
```
1. Backend (Unit 1) — 선행 개발
   └── API 완성 후 Frontend 개발 시작

2. Frontend (Unit 2) — 후행 개발
   └── Backend API에 의존
```

### 통합 포인트

| 통합 영역 | 방식 | 비고 |
|-----------|------|------|
| REST API | HTTP 호출 | Frontend → Backend (17개 엔드포인트) |
| SSE | EventSource | Admin Dashboard → Backend SSE 스트림 |
| 인증 | JWT Bearer Token | 요청 헤더에 토큰 포함 |
| CORS | FastAPI CORS 미들웨어 | Frontend 도메인 허용 |

### 통합 테스트 전략
- Backend 완성 후 API 단독 테스트 (curl/httpie)
- Frontend 개발 시 실제 Backend 연동 테스트
- SSE 연결 안정성 테스트

---

## 공유 계약 (API Contract)

Frontend가 Backend에 의존하는 핵심 계약:

| 계약 | 내용 |
|------|------|
| Base URL | `http://localhost:8000/api` |
| 인증 헤더 | `Authorization: Bearer {token}` |
| 응답 형식 | JSON |
| 에러 형식 | `{detail: string}` (FastAPI 기본) |
| SSE URL | `http://localhost:8000/api/sse/orders/{store_id}` |
| SSE 이벤트 | `new_order`, `order_updated`, `order_deleted`, `table_completed` |

---

## 리스크 및 완화

| 리스크 | 영향 | 완화 방안 |
|--------|------|-----------|
| API 스펙 변경 | Frontend 수정 필요 | Backend 먼저 완성하여 스펙 확정 |
| DynamoDB 로컬 설정 | 개발 환경 복잡도 | DynamoDB Local 사용 |
| SSE 연결 끊김 | 실시간 모니터링 중단 | 자동 재연결 로직 구현 |
