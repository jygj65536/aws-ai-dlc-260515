# Table Order Service - Backend

테이블 오더 서비스 백엔드 API (FastAPI + DynamoDB)

## 기술 스택

- **Framework**: FastAPI (Python 3.11+)
- **Database**: DynamoDB (로컬: DynamoDB Local)
- **Authentication**: JWT (python-jose) + bcrypt (passlib)
- **Validation**: Pydantic v2

## 환경 설정

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env
# .env 파일 편집 (필요 시)
```

## DynamoDB Local 실행

```bash
# Docker로 DynamoDB Local 실행
docker run -d -p 8000:8000 amazon/dynamodb-local

# 테이블 생성
python -m scripts.create_tables

# 시드 데이터 생성
python -m scripts.seed_data
```

## 서버 실행

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

API 문서: http://localhost:8080/docs

## 테스트 실행

```bash
pytest tests/ -v
```

## API 엔드포인트 (Auth)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/auth/admin/login` | 관리자 로그인 |
| POST | `/api/auth/table/login` | 테이블 태블릿 로그인 |
| GET | `/api/auth/me` | 현재 인증 정보 확인 |

## 테스트 계정

- **관리자**: store_id=`store-001`, username=`admin`, password=`admin1234`
- **테이블**: store_id=`store-001`, table_number=`1` or `2`, password=`1234`
