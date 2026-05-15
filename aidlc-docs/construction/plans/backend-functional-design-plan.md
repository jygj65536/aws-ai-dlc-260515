# Functional Design Plan - Backend (Unit 1)

## 계획 개요
백엔드 유닛의 상세 비즈니스 로직, 도메인 모델, 비즈니스 규칙을 설계합니다.

---

## 실행 계획

- [x] Step 1: 도메인 엔티티 정의 (domain-entities.md)
  - [x] DynamoDB 테이블별 엔티티 스키마 정의
  - [x] 엔티티 간 관계 정의
  - [x] PK/SK 패턴 및 인덱스 설계

- [x] Step 2: 비즈니스 로직 모델 (business-logic-model.md)
  - [x] 주문 생성 플로우 상세
  - [x] 세션 관리 로직 (시작/만료/종료)
  - [x] 이용 완료 처리 로직
  - [x] SSE 이벤트 발행 로직

- [x] Step 3: 비즈니스 규칙 (business-rules.md)
  - [x] 인증/인가 규칙
  - [x] 데이터 검증 규칙
  - [x] 상태 전이 규칙
  - [x] 세션 만료 규칙
