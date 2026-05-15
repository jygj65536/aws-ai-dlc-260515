# Unit of Work Plan - 테이블오더 서비스

## 계획 개요
테이블오더 서비스를 개발 가능한 유닛으로 분해하기 위한 계획입니다.

---

## Part 1: 질문 및 결정사항

### Question 1
유닛 분해 전략으로 어떤 접근을 선호하시나요?

A) 레이어 기반 (백엔드 유닛 + 프론트엔드 유닛)
B) 기능 도메인 기반 (주문 유닛, 메뉴 유닛, 테이블 유닛 등)
C) 배포 단위 기반 (독립 배포 가능한 서비스별)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

> AI 추천 근거: 모노레포 + 레이어드 아키텍처 결정에 부합. 소규모 MVP에서 도메인별 분리는 과도한 오버헤드.

### Question 2
유닛 간 개발 순서는?

A) 백엔드 먼저 완성 → 프론트엔드 개발 (순차)
B) 백엔드/프론트엔드 동시 개발 (병렬, API 계약 기반)
C) 기능별 수직 슬라이스 (메뉴 기능 전체 → 주문 기능 전체)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

> AI 추천 근거: 1인 개발 환경에서 백엔드 API 완성 후 프론트엔드 연동이 효율적. API 변경 최소화.

---

## Part 2: 실행 계획

- [x] Step 1: 유닛 정의 (unit-of-work.md)
  - [x] Unit 1: Backend (FastAPI) 정의
  - [x] Unit 2: Frontend (Next.js) 정의
  - [x] 코드 조직 전략 문서화

- [x] Step 2: 유닛 의존성 (unit-of-work-dependency.md)
  - [x] 유닛 간 의존성 매트릭스
  - [x] 개발 순서 및 통합 전략

- [x] Step 3: 스토리-유닛 매핑 (unit-of-work-story-map.md)
  - [x] 각 스토리를 유닛에 할당
  - [x] 매핑 완전성 검증

---

## 필수 산출물
- `aidlc-docs/inception/application-design/unit-of-work.md`
- `aidlc-docs/inception/application-design/unit-of-work-dependency.md`
- `aidlc-docs/inception/application-design/unit-of-work-story-map.md`
