# 컴포넌트 정의 (Components)

## 프로젝트 구조 개요

```
table-order/                    # 모노레포
├── backend/                    # FastAPI (Python)
│   ├── app/
│   │   ├── routers/           # API 엔드포인트 (Controller 레이어)
│   │   ├── services/          # 비즈니스 로직 (Service 레이어)
│   │   ├── repositories/      # 데이터 접근 (Repository 레이어)
│   │   ├── models/            # 데이터 모델/스키마
│   │   └── core/              # 설정, 인증, SSE
│   └── requirements.txt
└── frontend/                   # Next.js (TypeScript)
    ├── app/
    │   ├── customer/          # 고객용 페이지
    │   └── admin/             # 관리자용 페이지
    ├── components/            # 공유 UI 컴포넌트
    ├── lib/                   # 유틸리티, API 클라이언트
    └── package.json
```

---

## 백엔드 컴포넌트

### BE-1: Auth Router/Service/Repository
| 항목 | 내용 |
|------|------|
| **책임** | 관리자 인증, 테이블 태블릿 인증, JWT 토큰 발급/검증 |
| **레이어** | Router → Service → Repository |
| **의존** | DynamoDB (AdminUser, Table 테이블) |

### BE-2: Store Router/Service/Repository
| 항목 | 내용 |
|------|------|
| **책임** | 매장 정보 관리 |
| **레이어** | Router → Service → Repository |
| **의존** | DynamoDB (Store 테이블) |

### BE-3: Table Router/Service/Repository
| 항목 | 내용 |
|------|------|
| **책임** | 테이블 CRUD, 세션 시작/종료, 이용 완료 처리, 과거 내역 조회 |
| **레이어** | Router → Service → Repository |
| **의존** | DynamoDB (Table, TableSession, OrderHistory 테이블) |

### BE-4: Menu Router/Service/Repository
| 항목 | 내용 |
|------|------|
| **책임** | 메뉴/카테고리 CRUD, 메뉴 순서 관리 |
| **레이어** | Router → Service → Repository |
| **의존** | DynamoDB (Category, MenuItem 테이블) |

### BE-5: Order Router/Service/Repository
| 항목 | 내용 |
|------|------|
| **책임** | 주문 생성, 주문 상태 변경, 주문 조회, 주문 삭제, SSE 이벤트 발행 |
| **레이어** | Router → Service → Repository |
| **의존** | DynamoDB (Order, OrderItem 테이블), SSE Manager |

### BE-6: SSE Manager
| 항목 | 내용 |
|------|------|
| **책임** | SSE 연결 관리, 이벤트 브로드캐스트 (매장별) |
| **레이어** | Core 인프라 |
| **의존** | 없음 (Order Service에서 호출됨) |

---

## 프론트엔드 컴포넌트

### FE-1: Customer - Menu Page
| 항목 | 내용 |
|------|------|
| **책임** | 메뉴 조회, 카테고리 필터, 메뉴 상세 보기 |
| **라우트** | `/customer` (기본 화면) |

### FE-2: Customer - Cart
| 항목 | 내용 |
|------|------|
| **책임** | 장바구니 관리 (추가/삭제/수량 조절), 로컬 저장, 총 금액 계산 |
| **라우트** | `/customer/cart` |

### FE-3: Customer - Order
| 항목 | 내용 |
|------|------|
| **책임** | 주문 확정, 성공/실패 처리, 주문 내역 조회 |
| **라우트** | `/customer/orders` |

### FE-4: Admin - Login
| 항목 | 내용 |
|------|------|
| **책임** | 관리자 로그인, JWT 토큰 관리 |
| **라우트** | `/admin/login` |

### FE-5: Admin - Dashboard (Order Monitor)
| 항목 | 내용 |
|------|------|
| **책임** | 실시간 주문 모니터링(SSE), 테이블별 그리드, 주문 상태 변경 |
| **라우트** | `/admin/dashboard` |

### FE-6: Admin - Table Management
| 항목 | 내용 |
|------|------|
| **책임** | 테이블 설정, 주문 삭제, 이용 완료, 과거 내역 조회 |
| **라우트** | `/admin/tables` |

### FE-7: Admin - Menu Management
| 항목 | 내용 |
|------|------|
| **책임** | 메뉴 CRUD, 카테고리 관리, 순서 조정 |
| **라우트** | `/admin/menus` |

### FE-8: Shared Components
| 항목 | 내용 |
|------|------|
| **책임** | 공통 UI (Button, Card, Modal, Toast 등), API 클라이언트, 인증 유틸 |
| **위치** | `components/`, `lib/` |
