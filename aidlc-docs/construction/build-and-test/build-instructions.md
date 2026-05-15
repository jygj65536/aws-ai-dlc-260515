# Build Instructions

## Prerequisites
- **Python**: 3.11+ (권장 3.12)
- **Node.js**: 18+ (권장 20 LTS)
- **npm**: 9+
- **OS**: macOS / Linux / Windows

## Build Steps

### 1. Backend 의존성 설치

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Backend 환경 설정

```bash
cp .env.example .env
# .env 파일 수정 불필요 (기본값으로 로컬 실행 가능)
```

### 3. Backend 빌드 검증

```bash
cd backend
source venv/bin/activate
python -c "from app.main import app; print('✅ Backend 빌드 성공')"
```

### 4. Frontend 의존성 설치

```bash
cd frontend
npm install
```

### 5. Frontend 빌드

```bash
cd frontend
npm run build
```

### 6. 전체 빌드 검증

```bash
# Backend 서버 시작
cd backend && source venv/bin/activate
uvicorn app.main:app --port 8080 &

# Frontend 서버 시작
cd frontend
npm run dev -- -p 3000 &

# API 동작 확인
curl http://localhost:8080/health
# 예상 응답: {"status":"healthy"}

# 프록시 동작 확인
curl http://localhost:3000/api/stores/store-001
# 예상 응답: {"store_id":"store-001","name":"맛있는 식당",...}
```

## Build Artifacts
- **Backend**: Python 패키지 (venv/), SQLite DB (data/local.db)
- **Frontend**: `.next/` 빌드 디렉토리

## Troubleshooting

### pip install 실패 (bcrypt)
- **원인**: C 컴파일러 없음
- **해결**: `xcode-select --install` (macOS) 또는 `apt install build-essential` (Linux)

### npm run build 실패 (TypeScript 에러)
- **원인**: 타입 불일치
- **해결**: `npm run build` 출력에서 에러 위치 확인 후 수정

### Backend 임포트 에러
- **원인**: venv 미활성화 또는 의존성 미설치
- **해결**: `source venv/bin/activate && pip install -r requirements.txt`
