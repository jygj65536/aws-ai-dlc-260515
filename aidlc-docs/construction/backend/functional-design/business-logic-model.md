# Business Logic Model - Backend

## 1. 인증 로직

### 1.1 관리자 로그인
```
INPUT: store_id, username, password
PROCESS:
  1. AdminUser 조회 (PK: store_id, SK: username)
  2. 계정 잠금 확인 (locked_until > 현재시각이면 거부)
  3. bcrypt.verify(password, password_hash)
  4. 실패 시: login_attempts += 1, 5회 초과 시 locked_until = 현재 + 15분
  5. 성공 시: login_attempts = 0, JWT 토큰 생성 (payload: store_id, username, role="admin", exp=16h)
OUTPUT: {access_token, token_type: "bearer"}
ERROR: 401 (잘못된 자격증명), 423 (계정 잠금)
```

### 1.2 테이블 태블릿 로그인
```
INPUT: store_id, table_number, password
PROCESS:
  1. Table 조회 (GSI TableNumberIndex: store_id + table_number)
  2. bcrypt.verify(password, password_hash)
  3. 성공 시: JWT 토큰 생성 (payload: store_id, table_id, role="table", exp=16h)
  4. 현재 활성 세션 확인 (current_session_id)
  5. 활성 세션 없거나 만료됨 → session_id = null 반환 (첫 주문 시 세션 생성)
OUTPUT: {access_token, table_id, session_id (nullable)}
ERROR: 401 (잘못된 자격증명)
```

### 1.3 JWT 토큰 검증
```
INPUT: Authorization header (Bearer token)
PROCESS:
  1. 토큰 디코딩 (python-jose)
  2. exp 확인 (만료 시 401)
  3. payload에서 store_id, role 추출
OUTPUT: 인증된 사용자 컨텍스트 {store_id, user_id/table_id, role}
```

---

## 2. 주문 생성 로직

```
INPUT: store_id, table_id, session_id (nullable), items [{menu_id, name, quantity, price}]
PROCESS:
  1. 인증 확인 (테이블 토큰)
  2. 입력 검증:
     - items 비어있지 않음
     - 각 item: quantity > 0, price > 0
     - menu_id가 해당 매장에 존재하는지 확인
  3. 세션 처리:
     a. session_id가 null인 경우 (첫 주문):
        - 새 TableSession 생성 (status="active", expires_at=now+4h)
        - Table.current_session_id 업데이트
     b. session_id가 있는 경우:
        - 세션 유효성 확인 (status="active", expires_at > now)
        - 만료된 경우: 새 세션 생성 (위 a와 동일)
  4. 주문 번호 생성 (매장별 순번: StoreOrderIndex 카운트 + 1)
  5. total_amount 계산: sum(item.quantity * item.price)
  6. Order 저장 (PK: session_id, SK: order_id)
  7. TableSession.total_amount += order.total_amount
  8. SSE 이벤트 발행: {type: "new_order", data: order}
OUTPUT: {order_id, order_number, total_amount, session_id}
ERROR: 400 (검증 실패), 401 (미인증), 404 (메뉴 없음)
```

---

## 3. 주문 상태 변경 로직

```
INPUT: order_id, new_status ("preparing" | "completed")
PROCESS:
  1. 인증 확인 (관리자 토큰)
  2. Order 조회
  3. 상태 전이 검증:
     - pending → preparing ✅
     - preparing → completed ✅
     - pending → completed ✅ (건너뛰기 허용)
     - completed → * ❌ (완료 후 변경 불가)
     - preparing → pending ❌ (역방향 불가)
  4. Order.status 업데이트
  5. SSE 이벤트 발행: {type: "order_updated", data: {order_id, status}}
OUTPUT: {order_id, status}
ERROR: 400 (잘못된 상태 전이), 404 (주문 없음)
```

---

## 4. 주문 삭제 로직 (관리자)

```
INPUT: order_id
PROCESS:
  1. 인증 확인 (관리자 토큰)
  2. Order 조회 → session_id 획득
  3. Order 삭제
  4. TableSession.total_amount -= order.total_amount
  5. SSE 이벤트 발행: {type: "order_deleted", data: {order_id, table_id}}
OUTPUT: {success: true}
ERROR: 404 (주문 없음)
```

---

## 5. 이용 완료 처리 로직

```
INPUT: table_id
PROCESS:
  1. 인증 확인 (관리자 토큰)
  2. Table 조회 → current_session_id 획득
  3. 세션 없으면 에러 (이미 비어있음)
  4. 해당 세션의 모든 Order 조회 (PK: session_id)
  5. OrderHistory 생성:
     - table_id, session_id, orders (전체 주문 리스트), total_amount, completed_at=now
  6. 해당 세션의 모든 Order 삭제 (batch delete)
  7. TableSession.status = "completed", completed_at = now
  8. Table.current_session_id = null
  9. SSE 이벤트 발행: {type: "table_completed", data: {table_id}}
OUTPUT: {success: true, message: "이용 완료 처리됨"}
ERROR: 400 (활성 세션 없음), 404 (테이블 없음)
```

---

## 6. 세션 만료 처리 로직

```
TRIGGER: 주문 생성/조회 시 세션 유효성 체크 (Lazy Expiration)
PROCESS:
  1. TableSession.expires_at < 현재시각 확인
  2. 만료된 경우:
     - TableSession.status = "expired"
     - Table.current_session_id = null
     - (주문 데이터는 유지 — 관리자가 이용 완료로 정리)
  3. 새 주문 요청 시: 새 세션 자동 생성
NOTE: 별도 스케줄러 없이 요청 시점에 만료 확인 (Lazy 방식)
```

---

## 7. SSE 이벤트 관리 로직

```
CONNECTION:
  1. 관리자가 GET /api/sse/orders/{store_id} 요청
  2. SSEManager에 연결 등록 (store_id → connection set)
  3. 연결 유지 (keep-alive ping 30초 간격)
  4. 연결 종료 시 자동 제거

BROADCAST:
  1. 이벤트 발생 시 SSEManager.broadcast(store_id, event_type, data)
  2. 해당 store_id의 모든 활성 연결에 이벤트 전송
  3. 전송 실패한 연결은 자동 제거

EVENT FORMAT:
  event: {event_type}
  data: {json_payload}
  id: {event_id}

EVENT TYPES:
  - new_order: 새 주문 생성됨
  - order_updated: 주문 상태 변경됨
  - order_deleted: 주문 삭제됨
  - table_completed: 테이블 이용 완료됨
```

---

## 8. 메뉴 조회 로직

```
INPUT: store_id
PROCESS:
  1. Category 전체 조회 (PK: store_id, sort_order 정렬)
  2. MenuItem 전체 조회 (PK: store_id, is_available=true만)
  3. 카테고리별 메뉴 그룹핑
  4. sort_order 기준 정렬
OUTPUT: {categories: [{id, name, items: [{menu_id, name, price, description}]}]}
```

---

## 9. 과거 내역 조회 로직

```
INPUT: table_id, date_from (optional), date_to (optional)
PROCESS:
  1. 인증 확인 (관리자 토큰)
  2. OrderHistory 조회 (PK: table_id)
  3. date_from/date_to 필터 적용 (GSI DateIndex)
  4. completed_at 역순 정렬
OUTPUT: [{history_id, session_id, orders, total_amount, completed_at}]
```
