# Unit Test Execution

## Backend Unit Tests

### 실행 방법

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### 테스트 범위
| 모듈 | 테스트 파일 | 테스트 내용 |
|------|------------|------------|
| Auth Service | `tests/test_auth_service.py` | 관리자/테이블 로그인, 계정 잠금, JWT 생성 |
| Auth Router | `tests/test_auth_router.py` | API 엔드포인트 응답 검증 |
| Order Service | (추가 필요) | 주문 생성, 상태 변경, 삭제 |
| Menu Service | (추가 필요) | 메뉴/카테고리 CRUD |
| Table Service | (추가 필요) | 테이블 생성, 이용 완료 |

### 기대 결과
- **기존 테스트**: Auth 관련 테스트 통과
- **커버리지 목표**: 핵심 비즈니스 로직 80%+

### 테스트 실패 시
1. 에러 메시지에서 실패 위치 확인
2. 해당 서비스/리포지토리 코드 확인
3. 수정 후 재실행: `pytest tests/ -v --tb=short`

---

## Frontend Unit Tests

### 실행 방법

현재 프론트엔드에는 별도 테스트 프레임워크가 설정되어 있지 않습니다.
추후 필요 시 다음과 같이 설정:

```bash
cd frontend
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
npx jest
```

### 테스트 범위 (추후 추가 시)
- 컴포넌트 렌더링 테스트
- 장바구니 로직 (lib/cart.ts)
- API 클라이언트 (lib/api.ts)

---

## 커버리지 리포트

```bash
cd backend
source venv/bin/activate
pytest tests/ --cov=app --cov-report=html
# 리포트 위치: htmlcov/index.html
```
