# Integration Test Instructions

## Purpose
Backend API와 Frontend 간의 연동, 그리고 서비스 간 상호작용을 검증합니다.

## 사전 조건

```bash
# Backend 서버 실행
cd backend && source venv/bin/activate
uvicorn app.main:app --port 8080

# (별도 터미널) Frontend 서버 실행
cd frontend
npm run dev -- -p 3000
```

---

## Test Scenarios

### Scenario 1: 관리자 로그인 → 대시보드 접근

**설명**: 관리자가 로그인 후 JWT 토큰으로 보호된 API에 접근

```bash
# 1. 로그인
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"store_id":"store-001","username":"admin","password":"1234"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. 인증된 요청
curl -s http://localhost:8080/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
# 예상: {"user_type":"admin","store_id":"store-001",...}
```

### Scenario 2: 테이블 로그인 → 주문 생성 → SSE 수신

**설명**: 고객이 테이블에서 주문하면 관리자 대시보드에 실시간 알림

```bash
# 1. 테이블 로그인
TABLE_RESP=$(curl -s -X POST http://localhost:8080/api/auth/table/login \
  -H "Content-Type: application/json" \
  -d '{"store_id":"store-001","table_number":1,"password":"1111"}')
TABLE_ID=$(echo $TABLE_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['table_id'])")

# 2. SSE 연결 (백그라운드)
curl -s -N http://localhost:8080/api/sse/orders/store-001 &
SSE_PID=$!

# 3. 주문 생성
curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d "{\"store_id\":\"store-001\",\"table_id\":\"$TABLE_ID\",\"session_id\":null,\"items\":[{\"menu_id\":\"menu-001\",\"name\":\"김치찌개\",\"quantity\":1,\"price\":9000}]}"
# 예상: SSE 스트림에 new_order 이벤트 수신

# 4. 정리
kill $SSE_PID
```

### Scenario 3: 주문 생성 → 상태 변경 → 이용 완료

**설명**: 전체 주문 라이프사이클 테스트

```bash
# 1. 주문 생성
ORDER=$(curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"store_id":"store-001","table_id":"table-001","session_id":null,"items":[{"menu_id":"menu-002","name":"된장찌개","quantity":1,"price":8000}]}')
ORDER_ID=$(echo $ORDER | python3 -c "import sys,json; print(json.load(sys.stdin)['order_id'])")
SESSION_ID=$(echo $ORDER | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

# 2. 상태 변경 (pending → preparing)
curl -s -X PATCH "http://localhost:8080/api/orders/$ORDER_ID/status?session_id=$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"status":"preparing"}'
# 예상: {"order_id":"...","status":"preparing"}

# 3. 상태 변경 (preparing → completed)
curl -s -X PATCH "http://localhost:8080/api/orders/$ORDER_ID/status?session_id=$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
# 예상: {"order_id":"...","status":"completed"}

# 4. 이용 완료
curl -s -X POST "http://localhost:8080/api/tables/table-001/complete?store_id=store-001"
# 예상: {"success":true,"message":"이용 완료 처리됨"}

# 5. 이력 확인
curl -s "http://localhost:8080/api/tables/table-001/history"
# 예상: 이력 1건 이상
```

### Scenario 4: 메뉴 CRUD

```bash
# 1. 카테고리 생성
CAT=$(curl -s -X POST http://localhost:8080/api/categories \
  -H "Content-Type: application/json" \
  -d '{"store_id":"store-001","name":"신메뉴","sort_order":10}')
CAT_ID=$(echo $CAT | python3 -c "import sys,json; print(json.load(sys.stdin)['category_id'])")

# 2. 메뉴 생성
MENU=$(curl -s -X POST http://localhost:8080/api/menus \
  -H "Content-Type: application/json" \
  -d "{\"store_id\":\"store-001\",\"name\":\"새 메뉴\",\"price\":15000,\"description\":\"테스트\",\"category_id\":\"$CAT_ID\",\"sort_order\":1}")
MENU_ID=$(echo $MENU | python3 -c "import sys,json; print(json.load(sys.stdin)['menu_id'])")

# 3. 메뉴 수정
curl -s -X PUT "http://localhost:8080/api/menus/$MENU_ID?store_id=store-001" \
  -H "Content-Type: application/json" \
  -d '{"name":"수정된 메뉴","price":12000}'

# 4. 메뉴 삭제
curl -s -X DELETE "http://localhost:8080/api/menus/$MENU_ID?store_id=store-001"

# 5. 카테고리 삭제
curl -s -X DELETE "http://localhost:8080/api/categories/$CAT_ID?store_id=store-001"
```

### Scenario 5: Frontend → Backend 프록시

```bash
# Next.js 프록시를 통한 API 호출
curl -s http://localhost:3000/api/stores/store-001
# 예상: Backend와 동일한 응답

curl -s "http://localhost:3000/api/menus?store_id=store-001"
# 예상: 카테고리별 메뉴 목록
```

---

## Cleanup

```bash
# DB 초기화 (필요 시)
rm -rf backend/data/
# 서버 재시작하면 시드 데이터 자동 로드
```
