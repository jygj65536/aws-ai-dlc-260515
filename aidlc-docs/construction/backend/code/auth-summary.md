# Auth 기능 구현 요약

## 구현 범위
- **스토리**: US-9 (매장 인증), US-5 (테이블 자동 로그인/세션)
- **비즈니스 규칙**: AUTH-01 ~ AUTH-06 전체 적용

## 생성된 파일

### Core
| 파일 | 역할 |
|------|------|
| `app/core/security.py` | JWT 생성/검증, bcrypt 해싱/검증 |
| `app/core/dynamodb.py` | DynamoDB 클라이언트 초기화 |
| `app/config.py` | 환경변수 기반 설정 (pydantic-settings) |

### Models
| 파일 | 역할 |
|------|------|
| `app/models/auth.py` | 요청/응답 Pydantic 스키마 |

### Repositories
| 파일 | 역할 |
|------|------|
| `app/repositories/admin_user_repository.py` | AdminUser CRUD (잠금, 시도 횟수) |
| `app/repositories/table_repository.py` | Table 조회 (GSI 활용) |
| `app/repositories/session_repository.py` | TableSession 활성 세션 조회 |

### Services
| 파일 | 역할 |
|------|------|
| `app/services/auth_service.py` | 로그인 비즈니스 로직 (잠금, 검증, 토큰) |

### Routers
| 파일 | 역할 |
|------|------|
| `app/routers/auth.py` | 3개 엔드포인트 (admin/login, table/login, me) |

### Dependencies
| 파일 | 역할 |
|------|------|
| `app/dependencies.py` | 인증 미들웨어 (role 검증, 매장 격리) |

### Scripts
| 파일 | 역할 |
|------|------|
| `scripts/create_tables.py` | DynamoDB 테이블 생성 |
| `scripts/seed_data.py` | 테스트 초기 데이터 |

### Tests
| 파일 | 역할 |
|------|------|
| `tests/conftest.py` | pytest fixtures, moto DynamoDB 모킹 |
| `tests/test_auth_service.py` | auth_service 단위 테스트 (9개) |
| `tests/test_auth_router.py` | auth router 통합 테스트 (9개) |

## 비즈니스 규칙 적용 현황

| 규칙 | 구현 | 검증 |
|------|:----:|:----:|
| AUTH-01: 5회 실패 → 15분 잠금 | ✅ | ✅ 테스트 |
| AUTH-02: 관리자 JWT 16시간 만료 | ✅ | ✅ config |
| AUTH-03: 테이블 JWT 16시간 만료 | ✅ | ✅ config |
| AUTH-04: 관리자 전용 API 보호 | ✅ | ✅ dependency |
| AUTH-05: 테이블 전용 API 보호 | ✅ | ✅ dependency |
| AUTH-06: 매장 격리 | ✅ | ✅ dependency |
