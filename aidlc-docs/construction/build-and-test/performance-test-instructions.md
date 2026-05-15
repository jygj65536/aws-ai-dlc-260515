# Performance Test Instructions

## Purpose
소규모 MVP 로컬 배포 환경에서의 기본 성능 검증.

## Performance Requirements (MVP 기준)
- **응답 시간**: < 500ms (95th percentile)
- **동시 사용자**: 10명 이상 (테이블 10개 동시 주문)
- **SSE 이벤트 전달**: < 2초
- **에러율**: < 1%

## 간단한 부하 테스트 (curl 기반)

### 동시 주문 생성 테스트

```bash
# 10개 동시 주문 생성
for i in $(seq 1 10); do
  curl -s -X POST http://localhost:8080/api/orders \
    -H "Content-Type: application/json" \
    -d "{\"store_id\":\"store-001\",\"table_id\":\"table-001\",\"session_id\":null,\"items\":[{\"menu_id\":\"menu-001\",\"name\":\"김치찌개\",\"quantity\":1,\"price\":9000}]}" &
done
wait
echo "10개 동시 주문 완료"
```

### 응답 시간 측정

```bash
# 단일 요청 응답 시간
time curl -s http://localhost:8080/api/menus?store_id=store-001 > /dev/null
# 예상: real 0.0xxs (50ms 이내)

time curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"store_id":"store-001","table_id":"table-001","session_id":null,"items":[{"menu_id":"menu-001","name":"김치찌개","quantity":1,"price":9000}]}' > /dev/null
# 예상: real 0.0xxs (100ms 이내)
```

## 참고
- 본 프로젝트는 소규모 MVP (로컬 배포)이므로 별도 부하 테스트 도구(k6, JMeter) 미사용
- 프로덕션 배포 시 별도 성능 테스트 계획 수립 필요
