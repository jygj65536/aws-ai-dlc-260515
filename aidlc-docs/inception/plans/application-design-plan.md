# Application Design Plan - 테이블오더 서비스

## 계획 개요
테이블오더 서비스의 고수준 컴포넌트 식별 및 서비스 레이어 설계를 위한 계획입니다.

---

## Part 1: 설계 질문

아래 질문에 답변해 주세요. 각 `[Answer]:` 태그 뒤에 선택한 옵션의 알파벳을 입력해 주세요.

### Question 1
백엔드 API 구조를 어떻게 구성하시겠습니까?

A) 단일 FastAPI 앱에 라우터(Router)로 도메인 분리 (stores, tables, orders, menus, auth)
B) 도메인별 별도 FastAPI 앱 (마이크로서비스 스타일)
C) 단일 앱 + 레이어드 아키텍처 (Controller → Service → Repository)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 2
Next.js 프론트엔드 구조를 어떻게 구성하시겠습니까?

A) 단일 Next.js 앱에서 고객용(/customer)과 관리자용(/admin) 라우팅 분리
B) 고객용과 관리자용을 별도 Next.js 앱으로 분리
C) 모노레포에서 공유 컴포넌트 + 별도 앱 2개
X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 3
DynamoDB 테이블 설계 전략은?

A) Single-Table Design (하나의 테이블에 모든 엔티티, PK/SK 패턴)
B) Table-per-Entity (엔티티별 별도 테이블: Stores, Tables, Orders, Menus 등)
C) 하이브리드 (관련 엔티티 그룹별 테이블: 주문 관련 1개, 매장/메뉴 관련 1개)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 4
컴포넌트 간 통신 패턴은?

A) 동기 REST API 호출만 (프론트엔드 → 백엔드)
B) REST API + SSE (주문 모니터링용 실시간 스트림)
C) REST API + WebSocket (양방향 실시간 통신)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 5
프로젝트 전체 구조(모노레포 vs 멀티레포)는?

A) 모노레포 (하나의 저장소에 backend/ + frontend/ 디렉토리)
B) 멀티레포 (백엔드와 프론트엔드 별도 저장소)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Part 2: 설계 실행 계획 (답변 후 실행)

- [x] Step 1: 컴포넌트 식별 및 정의 (components.md)
  - [x] 백엔드 컴포넌트 식별
  - [x] 프론트엔드 컴포넌트 식별
  - [x] 각 컴포넌트 책임 정의

- [x] Step 2: 컴포넌트 메서드 정의 (component-methods.md)
  - [x] 백엔드 API 엔드포인트/메서드 시그니처
  - [x] 프론트엔드 주요 페이지/컴포넌트 인터페이스

- [x] Step 3: 서비스 레이어 설계 (services.md)
  - [x] 서비스 정의 및 오케스트레이션 패턴
  - [x] 서비스 간 상호작용

- [x] Step 4: 컴포넌트 의존성 (component-dependency.md)
  - [x] 의존성 매트릭스
  - [x] 데이터 흐름

- [x] Step 5: 통합 문서 (application-design.md)
  - [x] 전체 설계 통합 정리

---

## 필수 산출물
- `aidlc-docs/inception/application-design/components.md`
- `aidlc-docs/inception/application-design/component-methods.md`
- `aidlc-docs/inception/application-design/services.md`
- `aidlc-docs/inception/application-design/component-dependency.md`
- `aidlc-docs/inception/application-design/application-design.md`
