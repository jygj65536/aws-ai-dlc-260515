# Backend - Table Order API

테이블 주문 시스템 백엔드 (FastAPI + DynamoDB)

## 기술 스택

- **Framework**: FastAPI (Python 3.12)
- **Database**: DynamoDB (로컬 개발: DynamoDB Local)
- **실시간**: SSE (Server-Sent Events)
- **인증**: JWT (python-jose)

## 사전 요구사항

- Python 3.11+
- Docker (DynamoDB Local 실행용)

## 설치 및 실행

### 1. 가상환경 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

### 3. DynamoDB Local 실행

```bash
docker run -d -p 8000:8000 amazon/dynamodb-local
```

### 4. 테이블 생성

```bash
python -m scripts.create_tables
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --port 8080
```

## API 엔드포인트

### 주문 (Orders)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/orders` | 주문 생성 |
| GET | `/api/orders` | 주문 목록 조회 |
| PATCH | `/api/orders/{order_id}/status` | 주문 상태 변경 |
| DELETE | `/api/orders/{order_id}` | 주문 삭제 |

### SSE

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/sse/orders/{store_id}` | 실시간 주문 스트림 |

### 헬스 체크

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/health` | 서버 상태 확인 |

## API 문서

서버 실행 후:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 프로젝트 구조

```
backend/
├── app/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 환경변수 설정
│   ├── dependencies.py      # 의존성 주입
│   ├── core/
│   │   └── dynamodb.py      # DynamoDB 클라이언트
│   ├── models/
│   │   └── order.py         # Pydantic 스키마
│   ├── routers/
│   │   ├── orders.py        # 주문 API
│   │   └── sse.py           # SSE 스트림
│   ├── repositories/
│   │   ├── order_repository.py
│   │   ├── session_repository.py
│   │   ├── table_repository.py
│   │   └── order_history_repository.py
│   └── services/
│       ├── order_service.py  # 주문 비즈니스 로직
│       └── sse_manager.py    # SSE 연결 관리
├── scripts/
│   └── create_tables.py     # DB 테이블 생성
├── requirements.txt
└── .env.example
```
