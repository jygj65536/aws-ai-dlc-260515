# Unit of Work - Story Map

## 스토리-유닛 매핑

| Story ID | 스토리명 | Backend | Frontend | 비고 |
|----------|----------|:-------:|:--------:|------|
| US-1 | 메뉴 조회 및 탐색 | ✅ API | ✅ UI | Menu API + Customer Menu Page |
| US-2 | 장바구니 관리 | - | ✅ UI | 프론트엔드 로컬 저장만 |
| US-3 | 주문 생성 | ✅ API | ✅ UI | Order API + Customer Order Page |
| US-4 | 주문 내역 조회 | ✅ API | ✅ UI | Order API + Customer Orders Page |
| US-5 | 테이블 자동 로그인/세션 | ✅ API | ✅ UI | Auth API + 자동 로그인 로직 |
| US-6 | 실시간 주문 모니터링 | ✅ SSE | ✅ UI | SSE Manager + Admin Dashboard |
| US-7 | 테이블 관리 | ✅ API | ✅ UI | Table API + Admin Tables Page |
| US-8 | 메뉴 관리 | ✅ API | ✅ UI | Menu API + Admin Menus Page |
| US-9 | 매장 인증 | ✅ API | ✅ UI | Auth API + Admin Login Page |

---

## 유닛별 스토리 할당

### Unit 1: Backend
**모든 스토리의 API/서버 측 구현 담당** (US-2 제외)

| 우선순위 | 구현 순서 | 스토리 | 구현 내용 |
|:--------:|:---------:|--------|-----------|
| P1 | 1 | US-9 | Auth API (관리자 로그인, JWT) |
| P1 | 2 | US-5 | Auth API (테이블 로그인, 세션) |
| P1 | 3 | US-1 | Menu API (조회, 카테고리) |
| P1 | 4 | US-3 | Order API (생성) + SSE 이벤트 |
| P1 | 5 | US-6 | SSE Manager (실시간 스트림) |
| P1 | 6 | US-7 | Table API (관리, 이용 완료) |
| P2 | 7 | US-4 | Order API (내역 조회) |
| P2 | 8 | US-8 | Menu API (CRUD 관리) |

### Unit 2: Frontend
**모든 스토리의 UI/클라이언트 측 구현 담당**

| 우선순위 | 구현 순서 | 스토리 | 구현 내용 |
|:--------:|:---------:|--------|-----------|
| P1 | 1 | US-9 | Admin Login Page |
| P1 | 2 | US-5 | Customer 자동 로그인 |
| P1 | 3 | US-1 | Customer Menu Page |
| P1 | 4 | US-2 | Customer Cart (로컬 저장) |
| P1 | 5 | US-3 | Customer Order Page |
| P1 | 6 | US-6 | Admin Dashboard (SSE) |
| P1 | 7 | US-7 | Admin Tables Page |
| P2 | 8 | US-4 | Customer Orders History |
| P2 | 9 | US-8 | Admin Menus Page |

---

## 매핑 완전성 검증

- ✅ 모든 9개 스토리가 최소 1개 유닛에 할당됨
- ✅ US-2 (장바구니)는 Frontend 전용 (Backend 불필요)
- ✅ 나머지 8개 스토리는 Backend + Frontend 모두 관여
- ✅ 개발 순서가 의존성을 반영 (Auth → Menu → Order → Table)
