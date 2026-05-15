# Code Summary - Backend Order Feature

## 브랜치: feature/order

## 생성된 파일 목록

### 공통 인프라
| 파일 | 설명 |
|------|------|
| `backend/app/__init__.py` | 패키지 초기화 |
| `backend/app/main.py` | FastAPI 앱 진입점 |
| `backend/app/config.py` | 환경변수 설정 (pydantic-settings) |
| `backend/app/dependencies.py` | 의존성 주입 (인증 스텁 포함) |
| `backend/app/core/dynamodb.py` | DynamoDB 클라이언트 |
| `backend/requirements.txt` | Python 패키지 의존성 |
| `backend/.env.example` | 환경변수 예시 |

### 모델 (Pydantic 스키마)
| 파일 | 설명 |
|------|------|
| `backend/app/models/order.py` | 주문 요청/응답 스키마, OrderStatus enum |

### Repository 레이어
| 파일 | 설명 |
|------|------|
| `backend/app/repositories/order_repository.py` | Order 테이블 CRUD |
| `backend/app/repositories/session_repository.py` | TableSession 테이블 접근 |
| `backend/app/repositories/table_repository.py` | Table 테이블 접근 (세션 연결용) |
| `backend/app/repositories/order_history_repository.py` | OrderHistory 테이블 접근 |

### Service 레이어
| 파일 | 설명 |
|------|------|
| `backend/app/services/order_service.py` | 주문 비즈니스 로직 (생성, 조회, 상태변경, 삭제) |
| `backend/app/services/sse_manager.py` | SSE 연결 관리 및 브로드캐스트 |

### Router (API 엔드포인트)
| 파일 | 설명 |
|------|------|
| `backend/app/routers/orders.py` | 주문 REST API (CRUD) |
| `backend/app/routers/sse.py` | SSE 스트림 엔드포인트 |

### 스크립트
| 파일 | 설명 |
|------|------|
| `backend/scripts/create_tables.py` | DynamoDB 테이블 생성 |

### 문서
| 파일 | 설명 |
|------|------|
| `backend/README.md` | 백엔드 실행 가이드 |

---

## 구현된 비즈니스 로직

### 주문 생성 (US-3)
- 입력 검증 (Pydantic: items 1개 이상, quantity 1~99, price > 0)
- 세션 자동 생성/만료 처리 (Lazy Expiration)
- 주문 번호 자동 생성 (매장별 순번)
- 총액 서버 계산 (클라이언트 값 무시)
- SSE 이벤트 발행 (new_order)

### 주문 조회 (US-4)
- 세션별 조회 (고객용)
- 매장별 조회 (관리자용, GSI 활용)

### 주문 상태 변경 (US-6)
- 상태 전이 검증 (pending→preparing→completed, 건너뛰기 허용)
- 역방향/완료 후 변경 차단
- SSE 이벤트 발행 (order_updated)

### 주문 삭제 (US-7)
- 세션 총액 차감
- SSE 이벤트 발행 (order_deleted)

### SSE 실시간 스트림 (US-6)
- 매장별 연결 관리
- 30초 keep-alive ping
- 자동 연결 정리

---

## 인증 상태
- **현재**: 스텁 (개발 모드, 인증 없이 동작)
- **예정**: feature/auth 브랜치에서 JWT 기반 실제 인증 구현 후 머지

## 다른 브랜치에서 구현 예정
- Auth (feature/auth): 관리자/테이블 로그인, JWT 발급/검증
- Menu (feature/menu): 메뉴/카테고리 CRUD
- Table (feature/table): 테이블 관리, 이용 완료 처리
