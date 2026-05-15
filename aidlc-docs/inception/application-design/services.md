# 서비스 레이어 설계 (Services)

## 서비스 아키텍처 개요

```
[Frontend] → REST API → [Router] → [Service] → [Repository] → [DynamoDB]
                              ↓
                         [SSE Manager] → [Admin Dashboard]
```

레이어드 아키텍처 (Controller → Service → Repository):
- **Router (Controller)**: HTTP 요청/응답 처리, 입력 검증, 인증 확인
- **Service**: 비즈니스 로직, 트랜잭션 조율, 이벤트 발행
- **Repository**: DynamoDB 데이터 접근, 쿼리 실행

---

## 서비스 정의

### AuthService
| 항목 | 내용 |
|------|------|
| **책임** | 인증/인가 로직, JWT 토큰 생성/검증, 비밀번호 해싱/검증 |
| **주요 메서드** | `authenticate_admin()`, `authenticate_table()`, `create_token()`, `verify_token()` |
| **의존** | AdminUserRepository, TableRepository, JWT 라이브러리, bcrypt |

### StoreService
| 항목 | 내용 |
|------|------|
| **책임** | 매장 정보 관리 |
| **주요 메서드** | `get_store()` |
| **의존** | StoreRepository |

### TableService
| 항목 | 내용 |
|------|------|
| **책임** | 테이블 관리, 세션 라이프사이클, 이용 완료 처리 |
| **주요 메서드** | `create_table()`, `get_tables()`, `complete_table_session()`, `get_table_history()` |
| **의존** | TableRepository, SessionRepository, OrderRepository (이력 이동용) |
| **오케스트레이션** | 이용 완료 시: 세션 종료 → 주문 이력 이동 → 테이블 리셋 |

### MenuService
| 항목 | 내용 |
|------|------|
| **책임** | 메뉴/카테고리 CRUD, 순서 관리, 데이터 검증 |
| **주요 메서드** | `get_menus()`, `create_menu()`, `update_menu()`, `delete_menu()`, `reorder_menus()` |
| **의존** | MenuRepository, CategoryRepository |

### OrderService
| 항목 | 내용 |
|------|------|
| **책임** | 주문 생성, 상태 관리, 삭제, SSE 이벤트 트리거 |
| **주요 메서드** | `create_order()`, `get_orders()`, `update_order_status()`, `delete_order()` |
| **의존** | OrderRepository, SSEManager, TableService (총 주문액 계산) |
| **오케스트레이션** | 주문 생성 시: 주문 저장 → 세션 시작 확인 → SSE 이벤트 발행 |

### SSEManager
| 항목 | 내용 |
|------|------|
| **책임** | SSE 연결 풀 관리, 매장별 이벤트 브로드캐스트 |
| **주요 메서드** | `connect(store_id)`, `disconnect(store_id, connection_id)`, `broadcast(store_id, event)` |
| **의존** | 없음 (인메모리 연결 관리) |
| **이벤트 타입** | `new_order`, `order_updated`, `order_deleted`, `table_completed` |

---

## 서비스 간 상호작용

### 주문 생성 플로우
```
1. OrderRouter.create_order(request)
2. → OrderService.create_order(order_data)
3.   → OrderRepository.save(order)
4.   → TableService.ensure_session_active(table_id)  # 첫 주문 시 세션 시작
5.   → SSEManager.broadcast(store_id, "new_order", order)
6. ← Response: {order_id, order_number}
```

### 이용 완료 플로우
```
1. TableRouter.complete_table(table_id)
2. → TableService.complete_table_session(table_id)
3.   → OrderRepository.get_session_orders(session_id)
4.   → OrderHistoryRepository.save_batch(orders)  # 이력 이동
5.   → OrderRepository.delete_session_orders(session_id)
6.   → SessionRepository.close_session(session_id)
7.   → SSEManager.broadcast(store_id, "table_completed", table_id)
8. ← Response: {success}
```

### 주문 상태 변경 플로우
```
1. OrderRouter.update_status(order_id, status)
2. → OrderService.update_order_status(order_id, status)
3.   → OrderRepository.update_status(order_id, status)
4.   → SSEManager.broadcast(store_id, "order_updated", {order_id, status})
5. ← Response: {order_id, status}
```
