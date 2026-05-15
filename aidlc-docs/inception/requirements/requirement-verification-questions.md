# 요구사항 명확화 질문

아래 질문에 답변해 주세요. 각 질문의 `[Answer]:` 태그 뒤에 선택한 옵션의 알파벳을 입력해 주세요.
제공된 옵션 중 맞는 것이 없으면 마지막 옵션(Other)을 선택하고 설명을 추가해 주세요.

---

## Question 1
백엔드 서버 기술 스택으로 어떤 것을 사용하시겠습니까?

A) Node.js + Express (JavaScript/TypeScript)
B) Spring Boot (Java/Kotlin)
C) FastAPI / Django (Python)
D) NestJS (TypeScript)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
프론트엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) React (JavaScript/TypeScript)
B) Vue.js
C) Next.js (React 기반 풀스택 프레임워크)
D) Svelte / SvelteKit
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 3
데이터베이스로 어떤 것을 사용하시겠습니까?

A) PostgreSQL (관계형)
B) MySQL (관계형)
C) MongoDB (NoSQL Document)
D) DynamoDB (AWS NoSQL)
X) Other (please describe after [Answer]: tag below)

[Answer]: D

## Question 4
배포 환경은 어디를 대상으로 하시겠습니까?

A) AWS (EC2, ECS, Lambda 등)
B) 로컬/온프레미스 서버
C) Docker 컨테이너 기반 (클라우드 미정)
D) Vercel / Railway 등 PaaS
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 5
매장(Store) 관리 구조는 어떻게 되나요? (멀티테넌시)

A) 단일 매장만 지원 (MVP에서는 하나의 매장만 운영)
B) 다중 매장 지원 (하나의 시스템에서 여러 매장 독립 운영)
C) 단일 매장으로 시작하되, 향후 다중 매장 확장 가능한 구조
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 6
메뉴 이미지 관리는 어떻게 처리하시겠습니까?

A) 외부 이미지 URL 직접 입력 (별도 업로드 없음)
B) 서버에 이미지 파일 업로드 및 저장
C) AWS S3 등 클라우드 스토리지에 업로드
D) 이미지 없이 텍스트만으로 MVP 진행
X) Other (please describe after [Answer]: tag below)

[Answer]: D

## Question 7
고객용 인터페이스의 접근 방식은 어떻게 되나요?

A) 태블릿 전용 웹앱 (고정 URL로 접근)
B) QR코드 스캔으로 접근하는 모바일 웹
C) 태블릿 고정 URL + QR코드 모바일 접근 모두 지원
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 8
관리자 인터페이스 접근 방식은 어떻게 되나요?

A) 별도 웹 URL로 접근하는 관리자 전용 웹앱
B) 같은 앱 내에서 관리자 모드로 전환
C) 별도 데스크톱 앱
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 9
동시 접속 규모 예상은 어떻게 되나요? (MVP 기준)

A) 소규모 (테이블 10개 이하, 동시 주문 5건 이하)
B) 중규모 (테이블 10~30개, 동시 주문 10~20건)
C) 대규모 (테이블 30개 이상, 동시 주문 20건 이상)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 10
테이블 세션의 자동 만료 정책이 필요한가요?

A) 필요 없음 (관리자가 수동으로 "이용 완료" 처리만 함)
B) 일정 시간(예: 4시간) 후 자동 만료
C) 영업 시간 종료 시 일괄 만료
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 11: Security Extensions
이 프로젝트에 보안 확장 규칙을 적용하시겠습니까?

A) Yes — 모든 SECURITY 규칙을 blocking constraint로 적용 (프로덕션 수준 애플리케이션에 권장)
B) No — 모든 SECURITY 규칙 건너뛰기 (PoC, 프로토타입, 실험적 프로젝트에 적합)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 12: Property-Based Testing Extension
이 프로젝트에 Property-Based Testing (PBT) 규칙을 적용하시겠습니까?

A) Yes — 모든 PBT 규칙을 blocking constraint로 적용 (비즈니스 로직, 데이터 변환, 직렬화, 상태 관리 컴포넌트가 있는 프로젝트에 권장)
B) Partial — 순수 함수와 직렬화 round-trip에만 PBT 규칙 적용 (제한적 알고리즘 복잡도를 가진 프로젝트에 적합)
C) No — 모든 PBT 규칙 건너뛰기 (단순 CRUD, UI 전용, 비즈니스 로직이 적은 프로젝트에 적합)
X) Other (please describe after [Answer]: tag below)

[Answer]: C
