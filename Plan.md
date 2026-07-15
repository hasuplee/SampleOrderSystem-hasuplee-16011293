# Plan.md

이 문서는 SampleOrderSystem 프로젝트에서 수행되는 모든 액션(설계·문서화·구현·리팩터링 등)을
**실행 전에 먼저 기록**하고, 실행 후 결과를 이력으로 남기기 위한 문서입니다.

- 기능 구현에 관한 세부 RED/GREEN/REVIEW 계획은 `.claude/skills/test-driven-development/SKILL.md` 규칙을 따르며,
  해당 문서가 요구하는 Plan(목표/범위/테스트 계획)도 이 파일에 사이클 단위로 기록합니다.
- 그 외 모든 액션(문서 작성, 아키텍처 결정, 리팩터링 제안 등)도 실행 전 "진행 중" 항목으로 먼저 적고,
  완료되면 "이력"으로 이동시킵니다.
- 커밋은 사람 파트너의 명시적 확인 없이 실행하지 않습니다 (SKILL.md 준수).

## 진행 중 (Active)

### Cycle 1 — RED: Sample 모델 + SampleRepository

- **목표(goal)**: 시료(Sample)를 SQLite에 등록·조회·검색할 수 있다. 중복 ID 등록은 거부된다.
  (PRD.md 4.2절, 5절, 7절의 "시료 ID 유일성" 요구사항 충족)
- **범위(포함)**:
  - `model/sample.py`: `Sample` 데이터클래스 (sample_id, name, avg_production_time,
    yield_rate, stock=0)
  - `db/connection.py`: SQLite 연결 + `samples` 테이블 스키마 초기화
    (DataPersistence PoC 패턴 계승)
  - `repository/sample_repository.py`: `SampleRepository.create/get/list_all/search`
- **범위(제외, 이번 사이클에 하지 않음)**:
  - `update`/`delete` (재고 차감 등 향후 사이클에서 필요해지면 그때 추가 — YAGNI)
  - Order/ProductionJob 관련 일체
  - 콘솔 View/Controller 연동
- **테스트 계획** (`tests/repository/test_sample_repository.py`):
  1. `test_시료를_등록하면_저장된다` — create() 후 get()으로 조회하면 동일한 필드값 반환
  2. `test_존재하지_않는_시료_ID를_조회하면_None을_반환한다`
  3. `test_중복된_시료_ID로_등록하면_예외가_발생한다`
  4. `test_등록된_시료_목록을_조회할_수_있다` — list_all()이 등록 순서대로(또는 ID 순) 반환
  5. `test_이름으로_시료를_검색하면_부분일치하는_시료만_반환된다`
  - 모든 테스트는 `tmp_db_path` 픽스처(tests/conftest.py)로 격리된 SQLite 파일 사용, mock 없음.
- **승인**: 완료 (사람 파트너 승인).
- **RED 검증**: `tests/repository/test_sample_repository.py` 5개 테스트 작성 후
  `pytest tests/repository/test_sample_repository.py -v` 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.model.sample'`로 수집 단계에서
  실패. 오타가 아니라 `model/sample.py`, `repository/sample_repository.py`가 아직 존재하지
  않아서 발생하는 예상된 실패 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 1][RED]`, commit 3ec14b9).

### Cycle 1 — GREEN: 최소 구현

- **구현**: `model/sample.py`(Sample 데이터클래스), `db/connection.py`(SQLite 연결 +
  samples 테이블 스키마), `repository/sample_repository.py`(SampleRepository:
  create/get/list_all/search, 중복 ID는 `ValueError`).
- **범위 참고**: `search()`는 Plan의 테스트 요구사항(이름 부분일치)만 구현. PRD.md 4.2절은
  ID 부분일치도 언급하나 RED 테스트 목록에 없어 이번 GREEN에는 포함하지 않음 — REVIEW에서
  스코프로 다룸.
- **GREEN 검증**: `pytest tests/repository/test_sample_repository.py -v` → 5 passed.
  전체 스위트(`pytest`) → 5 passed(신규 5건 외 없음). `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음, GREEN 단계에서는 커밋하지 않음).

### Cycle 1 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음.
- **갭 발견**: PRD.md 4.2절(ID/이름 검색) 대비 `search()`가 이름만 지원. 스코프 크리프가
  아니라 PRD 대비 부족한 기능이라 사람 파트너에게 확인 → **"백로그로 남기고 지금은 이름
  검색만 유지"** 로 결정.
- **수행 내용**: `PRD.md` 4.2절에 TODO(백로그) 항목으로 ID 검색 확장 계획 명시.
- **리팩토링**: 없음 (코드 단순, REVIEW에서 즉시 필요한 정리 항목 없음).
- **REVIEW 후 테스트 재확인**: 전체 테스트 5 passed 유지.
- **커밋 시점 2**: 완료 (`[Cycle 1][GREEN+REVIEW]`, commit ee60799). Cycle 1 종료.

## 이력 (History) — 규칙 변경

### [2026-07-15] 커밋 규칙 → "커밋&푸쉬"로 확장

- **배경**: 사용자 지시. "커밋"이라고 되어 있던 기존 규칙(RED 종료/REVIEW 종료 시점, 승인 후
  수행)은 그대로 유지하되, 커밋 직후 `origin main` 푸쉬까지 하도록 확장.
- **수행 내용**: `CLAUDE.md`(Agentic Engineering 워크플로우 절, TDD 사이클 요약),
  `COMMIT_CONVENTION.md`(상단 갱신 안내) 반영. 원격 `origin`(GitHub) 존재 확인 후,
  아직 푸쉬되지 않았던 `ee60799`([Cycle 1][GREEN+REVIEW])까지 즉시 푸쉬 완료.
- **상태**: 완료. 이후 모든 커밋 시점에 동일하게 적용.

## 진행 중 (Active)

### Cycle 2 — RED: 시료 주문(Order) 생성 + 시료 ID 존재 검증

- **목표(goal)**: 고객이 등록된 시료로 주문하면 `RESERVED` 상태의 Order가 생성되고
  `ORD-####` 형식으로 순차 채번된다. 등록되지 않은 시료 ID로는 주문할 수 없다.
  (PRD.md 4.3절 — PoC ConsoleMVC의 "시료 ID 미검증" 결함 해소)
- **범위(포함)**:
  - `model/order.py`: `OrderStatus` Enum(RESERVED/REJECTED/PRODUCING/CONFIRMED/RELEASE),
    `Order` 데이터클래스
  - `db/connection.py`: `orders` 테이블 스키마 추가(samples FK)
  - `repository/order_repository.py`: `OrderRepository.create/get/next_order_id`
  - `service/order_service.py`: `OrderService(sample_repo, order_repo).create_order(sample_id,
    customer_name, quantity)` — 시료 존재 검증 → 다음 주문 ID 채번 → RESERVED로 생성/저장
- **범위(제외)**: 승인/거절, 재고 차감, 생산 큐, 출고, 콘솔 View/Controller — 이후 사이클.
- **테스트 계획** (`tests/service/test_order_service.py`, `tests/repository/test_order_repository.py`):
  1. `test_등록된_시료로_주문하면_RESERVED_상태로_생성된다`
  2. `test_등록되지_않은_시료_ID로_주문하면_예외가_발생한다`
  3. `test_주문_ID는_ORD_형식으로_순차_채번된다` (두 건 생성 시 ORD-0001, ORD-0002)
  4. `test_생성된_주문을_조회하면_저장된_값과_동일하다`
  - `tmp_db_path` 픽스처 사용, mock 없음. 시료는 `SampleRepository`로 사전 등록 후 사용.
- **승인**: 완료 (사람 파트너 승인).
- **RED 검증**: `tests/service/test_order_service.py`(3건), `tests/repository/test_order_repository.py`
  (1건) 작성 후 실행 → `ModuleNotFoundError: No module named 'sample_order_system.model.order'`로
  수집 단계에서 실패. `model/order.py`, `repository/order_repository.py`,
  `service/order_service.py`가 아직 없어서 발생하는 예상된 실패 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 2][RED]`, commit 84cb6dd, 푸쉬 완료).

### Cycle 2 — GREEN: 최소 구현

- **구현**: `model/order.py`(OrderStatus, Order), `db/connection.py`(orders 테이블 스키마
  추가), `repository/order_repository.py`(OrderRepository: create/get/next_order_id),
  `service/order_service.py`(OrderService.create_order — 시료 존재 검증 → 채번 → RESERVED 생성).
- **GREEN 검증**: 전체 스위트(`pytest`) → 9 passed (기존 5건 + 신규 4건). `ruff check src tests`
  → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 2 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음 (승인/거절, 재고, 생산 큐, View/Controller
  모두 손대지 않음).
- **리팩토링**: 없음.
- **참고**: `CLAUDE.md`/`COMMIT_CONVENTION.md`의 "커밋&푸쉬" 규칙 반영분이 아직 커밋되지 않은
  상태 — Cycle 2 REVIEW 커밋에 함께 포함할지 사람 파트너에게 확인 필요.
- **REVIEW 후 테스트 재확인**: 전체 테스트 9 passed 유지.
- **커밋 분리 결정**: 사람 파트너 지시로 문서 변경(커밋&푸쉬 규칙 반영)과 기능 구현을
  커밋 2번(각각 `[DOCS]`, `[Cycle 2][GREEN+REVIEW]`) + 푸쉬 1번으로 분리 처리.
- **커밋 시점 2**: 완료 (`[DOCS]` commit 99294cb, `[Cycle 2][GREEN+REVIEW]` commit 307cecd,
  푸쉬 1회로 두 커밋 모두 반영). Cycle 2 종료.

## 진행 중 (Active)

### Cycle 3 — RED: 주문 승인/거절 + 재고충분 시 CONFIRMED 전환·차감

- **목표(goal)**: RESERVED 주문을 거절하면 REJECTED로 전환된다. 승인 시 재고가 주문 수량
  이상이면 즉시 CONFIRMED로 전환되고, 확정된 정책(PRD 4.4)에 따라 재고가 주문 수량만큼
  차감된다. 재고 부족 케이스는 Cycle 4에서 다루므로 이번 사이클에서는 명시적으로
  `NotImplementedError`를 발생시켜 미구현 상태를 드러낸다(조용히 잘못된 상태로 넘어가지
  않도록 하는 경계 표시).
- **범위(포함)**:
  - `repository/sample_repository.py`에 `update(sample)` 추가 (재고 변경 저장)
  - `repository/order_repository.py`에 `update(order)` 추가 (상태 변경 저장)
  - `service/approval_service.py` 신규: `ApprovalService(sample_repo, order_repo)`
    - `reject_order(order_id)`: 주문을 `REJECTED`로 전환
    - `approve_order(order_id)`: 재고 충분 시 `CONFIRMED` 전환 + 재고 차감,
      재고 부족 시 `NotImplementedError`
- **범위(제외)**: 재고 부족 시 생산 큐 등록/실생산량 계산(Cycle 4), 생산완료 처리(Cycle 5),
  출고 처리(Cycle 6), 모니터링(Cycle 7), View/Controller.
- **테스트 계획**:
  - `tests/repository/test_sample_repository.py` 추가: `test_시료_정보를_수정하면_저장된다`
  - `tests/repository/test_order_repository.py` 추가: `test_주문_상태를_변경하면_저장된다`
  - `tests/service/test_approval_service.py` 신규:
    1. `test_주문을_거절하면_REJECTED_상태로_변경된다`
    2. `test_재고가_충분하면_승인시_CONFIRMED_상태로_변경된다`
    3. `test_재고가_충분하면_승인시_재고가_주문수량만큼_차감된다`
    4. `test_재고가_부족하면_승인시_NotImplementedError가_발생한다`
  - `tmp_db_path` 픽스처 사용, mock 없음.
- **승인**: 완료 (사용자가 "Cycle 3 계획대로 진행해줘"로 승인).
- **RED 검증**: 신규 테스트 6건(`test_시료_정보를_수정하면_저장된다`,
  `test_주문_상태를_변경하면_저장된다`, `test_approval_service.py` 4건) 작성 후 실행 →
  repository 2건은 `AttributeError: 'SampleRepository'/'OrderRepository' object has no
  attribute 'update'`, service 4건은 `ModuleNotFoundError: No module named
  'sample_order_system.service.approval_service'`로 예상대로 실패. 기존 8건은 그대로 통과 —
  RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 3][RED]`, commit 161844c, 푸쉬 완료).

### Cycle 3 — GREEN: 최소 구현

- **구현**: `repository/sample_repository.py`에 `update()` 추가,
  `repository/order_repository.py`에 `update()` 추가, `service/approval_service.py` 신규
  (`ApprovalService.reject_order/approve_order` — 재고 충분 시 CONFIRMED 전환·차감,
  재고 부족 시 `NotImplementedError`).
- **GREEN 검증**: 전체 스위트(`pytest`) → 15 passed (기존 9건 + 신규 6건).
  `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 3 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음.
- **갭 발견**: 존재하지 않는 `order_id`로 승인/거절 시 `AttributeError`가 발생하는 문제 발견
  (원래 테스트 목록에 없던 케이스). 사람 파트너에게 확인 → **"지금 테스트 추가해 바로 명확한
  예외로 처리"** 로 결정.
- **추가 RED→GREEN**: `test_존재하지_않는_주문을_승인하면_예외가_발생한다`,
  `test_존재하지_않는_주문을_거절하면_예외가_발생한다` 추가 → RED 확인
  (`AttributeError`가 발생해 `pytest.raises(ValueError)` 불일치로 실패) →
  `ApprovalService._get_order_or_raise()` 헬퍼 추가로 `ValueError` 발생하도록 수정 → GREEN 확인.
- **리팩토링**: `reject_order`/`approve_order` 공통 로직을 `_get_order_or_raise()`로 추출
  (중복 제거).
- **REVIEW 후 테스트 재확인**: 전체 테스트 17 passed. `ruff check` All checks passed.
- **커밋 시점 2**: 완료 (`[Cycle 3][GREEN+REVIEW]`, commit 97732a7, 푸쉬 완료). Cycle 3 종료.

## 진행 중 (Active)

### Cycle 4 — RED: 재고부족 시 생산 큐 등록 (실생산량/총생산시간 계산)

- **목표(goal)**: 승인 시 재고가 부족하면 Cycle 3의 `NotImplementedError` 대신, 부족분에
  대한 생산 작업(ProductionJob)이 FIFO 생산 큐에 등록되고 주문 상태가 `PRODUCING`으로
  전환된다. 실생산량 = `ceil(부족분 / 수율)`, 총 생산시간 = 평균생산시간 × 실생산량
  (PRD.md 4.4, 4.6절).
- **아키텍처 참고사항**: 생산 큐는 PoC ConsoleMVC와 동일하게 프로세스 메모리 내 FIFO
  큐(`ProductionQueue`)로 구현한다(콘솔 세션 동안만 유지). Sample/Order처럼 SQLite에
  영속화하지 않음 — 이는 알려진 제한사항으로 PRD.md에 남기고, 필요 시 이후 사이클에서
  재검토한다.
- **범위(포함)**:
  - `model/production_job.py`: `ProductionJob` 데이터클래스
    (order_id, sample_id, shortage_qty, actual_qty, total_time_min)
  - `model/production_queue.py`: `ProductionQueue` (enqueue/dequeue/peek/list_all, FIFO)
  - `service/approval_service.py` 수정: 생성자에 `production_queue` 파라미터 추가.
    `approve_order()`의 재고부족 분기를 `NotImplementedError`에서 실제 구현으로 교체
    (부족분/실생산량/총생산시간 계산 → ProductionJob 생성 → 큐 등록 → 주문 `PRODUCING` 전환)
- **범위(제외)**: 생산완료 처리(Cycle 5), 출고(Cycle 6), 모니터링(Cycle 7), View/Controller,
  생산 큐 영속화.
- **기존 테스트 변경 예정**: `tests/service/test_approval_service.py`의
  `test_재고가_부족하면_승인시_NotImplementedError가_발생한다`는 이번 사이클에서 실제 동작
  검증 테스트로 교체된다(자리표시자였던 Cycle 3 동작이 실제 구현으로 대체되므로). 기존
  `ApprovalService(...)` 생성 호출부에 `production_queue` 인자 추가 필요.
- **테스트 계획**:
  - `tests/model/test_production_queue.py` 신규:
    1. `test_생산_큐는_등록한_순서대로_작업을_반환한다` (FIFO)
    2. `test_빈_생산_큐에서_dequeue하면_None을_반환한다`
    3. `test_peek은_큐를_변경하지_않고_첫_작업을_반환한다`
  - `tests/service/test_approval_service.py` 추가/교체:
    4. `test_재고가_부족하면_승인시_생산_큐에_작업이_등록된다`
       (shortage_qty/actual_qty(ceil)/total_time_min 값 검증)
    5. `test_재고가_부족하면_승인시_주문_상태가_PRODUCING으로_변경된다`
  - `tmp_db_path` 픽스처 사용, mock 없음.
- **승인**: 완료 (사용자가 "Cycle 4 계획대로 진행해줘"로 승인).
- **RED 검증**: `tests/model/test_production_queue.py`(3건 신규),
  `tests/service/test_approval_service.py`(NotImplementedError 테스트 1건을 실제 동작
  테스트 2건으로 교체, 헬퍼에 ProductionQueue 주입 추가) 작성 후 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.model.production_job'`/
  `'...production_queue'`로 수집 단계에서 예상대로 실패. 기존 repository/order_service
  테스트 11건은 영향 없이 그대로 통과 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 4][RED]`, commit 78a26ca, 푸쉬 완료).

### Cycle 4 — GREEN: 최소 구현

- **구현**: `model/production_job.py`(ProductionJob), `model/production_queue.py`
  (ProductionQueue: enqueue/dequeue/peek/list_all), `service/approval_service.py` 수정
  (생성자에 `production_queue` 추가, 재고부족 분기를 `_enqueue_production_job()`으로 구현 —
  부족분/실생산량(ceil)/총생산시간 계산 → 큐 등록 → 주문 `PRODUCING` 전환).
- **GREEN 검증**: 전체 스위트(`pytest`) → 21 passed (기존 17건 + 신규/교체 4건).
  `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 4 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음.
- **리팩토링**: `approve_order()`의 두 분기가 `_enqueue_production_job()`으로 이미 분리되어
  있어 추가 정리 불필요.
- **갭**: 이번 사이클은 발견된 갭 없음.
- **REVIEW 후 테스트 재확인**: 전체 테스트 21 passed 유지. `ruff check` All checks passed.
- **커밋 시점 2**: 완료 (`[Cycle 4][GREEN+REVIEW]`, commit 299a2d1, 푸쉬 완료). Cycle 4 종료.

## 진행 중 (Active)

### Cycle 5 — RED: 생산완료 처리 (재고 증가 → CONFIRMED 전환·차감 → 큐 제거)

- **목표(goal)**: 담당자가 생산 큐의 현재 작업(맨 앞)을 수동으로 "생산완료 처리"하면:
  1) 대상 시료 재고가 `actual_qty`만큼 증가하고, 2) 해당 주문이 `CONFIRMED`로 전환되며
  주문 수량만큼 재고가 차감되고, 3) 생산 큐에서 해당 작업이 제거된다. (PRD.md 4.6절 확정 정책)
- **범위(포함)**:
  - `service/production_service.py` 신규: `ProductionService(sample_repo, order_repo,
    production_queue).complete_current_job()`
    - 큐가 비어있으면 `ValueError`
    - 큐 맨 앞 작업을 dequeue → 시료 재고 += `actual_qty` → 주문 조회 →
      재고 -= `order.quantity` → 주문 상태 `CONFIRMED` → 두 저장소에 update
- **범위(제외)**: 출고 처리(Cycle 6), 모니터링(Cycle 7), View/Controller.
- **테스트 계획** (`tests/service/test_production_service.py`):
  1. `test_생산완료_처리하면_재고가_실생산량만큼_증가한_뒤_주문수량만큼_차감된다`
     (순증감 = 원래재고 + actual_qty − 주문수량)
  2. `test_생산완료_처리하면_주문_상태가_CONFIRMED로_변경된다`
  3. `test_생산완료_처리하면_생산_큐에서_작업이_제거된다`
  4. `test_생산_큐가_비어있으면_생산완료_처리시_예외가_발생한다`
  - `tmp_db_path` 픽스처 사용, mock 없음. `ApprovalService.approve_order()`로 재고부족
    주문을 만들어 큐에 작업을 채운 뒤 검증.
- **승인**: 완료 (사용자가 "Cycle 5 계획대로 진행해줘"로 승인).
- **RED 검증**: `tests/service/test_production_service.py`(4건 신규) 작성 후 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.service.production_service'`로
  예상대로 실패. 기존 테스트 21건은 영향 없이 그대로 통과 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 5][RED]`, commit 58a4075, 푸쉬 완료).

### Cycle 5 — GREEN: 최소 구현

- **구현**: `service/production_service.py` 신규 (`ProductionService.complete_current_job()`
  — 큐 dequeue, 없으면 ValueError, 시료 재고 += actual_qty 후 -= 주문수량, 주문 CONFIRMED
  전환, 두 저장소 update).
- **GREEN 검증**: 전체 스위트(`pytest`) → 25 passed (기존 21건 + 신규 4건).
  `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 5 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음.
- **리팩토링**: 코드 단순, 즉시 필요한 정리 없음.
- **갭**: 이번 사이클은 발견된 갭 없음.
- **REVIEW 후 테스트 재확인**: 전체 테스트 25 passed 유지. `ruff check` All checks passed.
- **커밋 시점 2**: 완료 (`[Cycle 5][GREEN+REVIEW]`, commit dff6a8f, 푸쉬 완료). Cycle 5 종료.

## 진행 중 (Active)

### Cycle 6 — RED: 출고 처리 (CONFIRMED → RELEASE)

- **목표(goal)**: CONFIRMED 상태 주문을 출고 처리하면 `RELEASE`로 전환된다. 재고는 이미
  CONFIRMED 전환 시점에 차감되었으므로(Cycle 3/5) 출고 시점에는 추가로 변경하지 않는다
  (PRD.md 4.7절).
- **범위(포함)**:
  - `service/shipment_service.py` 신규: `ShipmentService(order_repository).release_order(
    order_id)`
    - 존재하지 않는 주문 → `ValueError`
    - `CONFIRMED`가 아닌 주문(예: RESERVED, PRODUCING, REJECTED, 이미 RELEASE) → `ValueError`
      (승인/거절 사이클에서 이미 확립한 "잘못된 상태 전이는 명확한 예외로 막는다" 패턴을
      동일하게 적용)
    - 정상 시 상태를 `RELEASE`로 전환하고 저장
- **범위(제외)**: 모니터링(Cycle 7), View/Controller.
- **테스트 계획** (`tests/service/test_shipment_service.py`):
  1. `test_CONFIRMED_주문을_출고처리하면_RELEASE_상태로_변경된다`
  2. `test_존재하지_않는_주문을_출고처리하면_예외가_발생한다`
  3. `test_CONFIRMED가_아닌_주문을_출고처리하면_예외가_발생한다`
  - `tmp_db_path` 픽스처 사용, mock 없음.
- **승인**: 완료 (사용자가 "Cycle 6 계획대로 진행해줘"로 승인).
- **RED 검증**: `tests/service/test_shipment_service.py`(3건 신규) 작성 후 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.service.shipment_service'`로
  예상대로 실패. 기존 테스트 25건은 영향 없이 그대로 통과 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 6][RED]`, commit 397ea53, 푸쉬 완료).

### Cycle 6 — GREEN: 최소 구현

- **구현**: `service/shipment_service.py` 신규 (`ShipmentService.release_order()` — 존재
  검증, CONFIRMED 상태 검증, RELEASE 전환).
- **GREEN 검증**: 전체 스위트(`pytest`) → 28 passed (기존 25건 + 신규 3건).
  `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 6 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 구현 없음.
- **리팩토링**: 코드 단순, 즉시 필요한 정리 없음.
- **갭**: 이번 사이클은 발견된 갭 없음.
- **REVIEW 후 테스트 재확인**: 전체 테스트 28 passed 유지. `ruff check` All checks passed.
- **커밋 시점 2**: 완료 (`[Cycle 6][GREEN+REVIEW]`, commit 10161f4, 푸쉬 완료). Cycle 6 종료.

## 진행 중 (Active)

### Cycle 7 — RED: 모니터링 (상태별 집계, 재고상태 계산)

- **목표(goal)**: 상태별 주문 건수(RESERVED/CONFIRMED/PRODUCING/RELEASE, REJECTED 제외)를
  집계하고, 시료별 재고 상태(여유/부족/고갈)와 잔여율을 계산할 수 있다. 재고 상태는
  대기수요(RESERVED+PRODUCING 주문 수량 합) 대비로 판단한다(PRD.md 4.5절 — PoC
  ConsoleMVC의 고정 임계치 방식이 아니라 DataMonitor 방식으로 통일하기로 확정된 정책).
- **범위(포함)**:
  - `service/monitoring_service.py` 신규:
    - `MonitoringService(sample_repository, order_repository)`
    - `status_counts() -> dict`: RESERVED/CONFIRMED/PRODUCING/RELEASE 건수, REJECTED 제외
    - `stock_states() -> list[dict]`: 시료별 sample_id/name/stock/pending_demand/state/ratio
      - `고갈`: stock == 0 / `부족`: stock < pending_demand / `여유`: 그 외
      - `ratio`: demand==0이면 1.0, 아니면 `min(1.0, stock/demand)`
- **범위(제외)**: View/Controller(콘솔 출력 형식은 Cycle 8).
- **테스트 계획** (`tests/service/test_monitoring_service.py`):
  1. `test_상태별_주문_건수를_집계할_수_있다` (RESERVED/CONFIRMED/PRODUCING/RELEASE 각각
     생성 + REJECTED 1건도 만들어 집계에서 제외되는지 함께 검증)
  2. `test_재고가_0이면_고갈_상태이다`
  3. `test_재고가_대기수요보다_적으면_부족_상태이다`
  4. `test_재고가_대기수요_이상이면_여유_상태이다`
  - `tmp_db_path` 픽스처 사용, mock 없음. 상태 조작은 `OrderRepository.update()`로 직접
    설정(이미 검증된 저장소 API를 테스트 셋업에 사용, mock 아님).
- **승인**: 완료 (사용자가 "Cycle 7 계획대로 진행해줘"로 승인).
- **RED 검증**: `tests/service/test_monitoring_service.py`(4건 신규) 작성 후 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.service.monitoring_service'`로
  예상대로 실패. 기존 테스트 28건은 영향 없이 그대로 통과 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 7][RED]`, commit 4fc1584, 푸쉬 완료).

### Cycle 7 — GREEN: 최소 구현

- **구현**: `service/monitoring_service.py` 신규 (`status_counts()`, `stock_states()`).
  구현 중 `OrderRepository`에 `list_all()`이 없다는 사전 의존성 누락을 발견해
  `SampleRepository.list_all()`과 동일한 패턴으로 추가(Plan에 명시되지 않았던 최소 보강,
  MonitoringService의 필수 전제조건이라 REVIEW에서 스코프로 다룸).
- **GREEN 검증**: 전체 스위트(`pytest`) → 32 passed (기존 28건 + 신규 4건).
  `ruff check src tests` → All checks passed.
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 7 — REVIEW

- **스코프 검토**: `OrderRepository.list_all()` 추가는 Plan.md에 명시적으로 적혀있지
  않았으나, `MonitoringService`가 반드시 필요로 하는 최소 의존성이라 스코프 크리프로
  보지 않고 그대로 유지하기로 판단(이미 `SampleRepository`에 동일 패턴이 존재해 일관성
  있음).
- **리팩토링**: 코드 단순, 즉시 필요한 정리 없음.
- **갭**: 이번 사이클은 추가 발견된 갭 없음.
- **REVIEW 후 테스트 재확인**: 전체 테스트 32 passed 유지. `ruff check` All checks passed.
- **커밋 시점 2**: 완료 (`[Cycle 7][GREEN+REVIEW]`, commit b9a88a7, 푸쉬 완료). Cycle 7 종료.

## 진행 중 (Active)

### Cycle 8 — RED: 콘솔 View/Controller 통합 (메인 메뉴, 입력 검증)

- **목표(goal)**: PRD.md 4.1절의 메인 메뉴(시료 관리/시료 주문/승인·거절/모니터링/생산라인
  조회/출고 처리)를 콘솔에서 실제로 조작할 수 있고, PRD.md 7절에 남아있던 PoC 갭
  "입력값 검증 부족"이 해소된다(숫자 아닌 입력, 범위 밖 선택 시 프로그램이 죽지 않고
  재입력을 요구).
- **테스트 범위에 대한 판단(중요)**: 이 사이클은 두 가지 성격의 코드가 섞여 있다.
  1) **순수 로직** — 원시 입력 문자열을 검증/파싱하는 함수(메뉴 선택 검증, 양의 정수
     파싱). 입출력 부수효과가 없어 TDD로 사전 테스트 가능 → 아래 테스트 계획 대상.
  2) **입출력 글루 코드** — `input()`/`print()`로 실제 터미널과 상호작용하는
     View 출력 함수와 메뉴 루프(Controller). 이 부분은 PoC ConsoleMVC 구조를 그대로
     계승해 서비스 계층(Cycle 1~7에서 이미 TDD로 검증됨)을 호출하는 얇은 배선(wiring)
     이며, 순수 로직처럼 미리 실패 테스트를 작성하기보다 **구현 후 실제 실행으로
     골든 패스를 수동 검증**한다(자동화된 대화형 입출력 테스트는 가치 대비 비용이
     크다고 판단 — TDD 예외: "일회성/자동 생성에 준하는 순수 배선 코드"). 완료 후
     `verify` 스킬로 실제 실행 결과를 이 대화에서 보고한다.
  - 이 판단 자체가 설계 결정이라 사람 파트너 승인 대상에 포함한다.
- **범위(포함)**:
  - `view/input_parsing.py`: `parse_menu_choice(raw, valid_choices)`,
    `parse_positive_int(raw)` — 순수 함수, TDD 대상
  - `view/*.py`, `controller/*.py`, `main.py`: 기존 서비스(OrderService, ApprovalService,
    ProductionService, ShipmentService, MonitoringService, SampleRepository,
    OrderRepository, ProductionQueue)를 호출하는 콘솔 메뉴 루프. 잘못된 입력 시
    `input_parsing`의 파싱 결과가 `None`이면 재입력을 요구(프로그램 종료 없음).
- **범위(제외)**: 신규 비즈니스 로직 없음(전부 기존 서비스 재사용). 여러 사용자 동시 접속,
  권한/로그인 분리는 PRD에 없으므로 제외.
- **테스트 계획** (`tests/view/test_input_parsing.py`):
  1. `test_유효한_메뉴_선택이면_그대로_반환한다`
  2. `test_유효하지_않은_메뉴_선택이면_None을_반환한다`
  3. `test_양의_정수_문자열이면_정수로_변환한다`
  4. `test_숫자가_아니면_None을_반환한다`
  5. `test_0_이하의_정수이면_None을_반환한다`
  - mock 없음, 입출력 부수효과 없는 순수 함수만 대상.
- **승인**: 완료. 사람 파트너가 "테스트 범위 판단"(순수 로직만 TDD, 메뉴 루프/main.py는
  구현 후 수동 검증)에 명시적으로 동의함.
- **RED 검증**: `tests/view/test_input_parsing.py`(5건 신규) 작성 후 실행 →
  `ModuleNotFoundError: No module named 'sample_order_system.view.input_parsing'`로
  예상대로 실패. 기존 테스트 32건은 영향 없이 그대로 통과 — RED 확인됨.
- **커밋 시점 1**: 완료 (`[Cycle 8][RED]`, commit 2760a7b, 푸쉬 완료).

### Cycle 8 — GREEN: 최소 구현

- **순수 로직 구현**: `view/input_parsing.py`(parse_menu_choice, parse_positive_int) —
  RED 테스트 5건을 만족하는 최소 구현.
- **입출력 글루 코드 구현(합의된 대로 사전 테스트 없이 구현 후 수동 검증)**:
  - `view/prompts.py`(read_menu_choice/read_positive_int/read_non_negative_int/read_float/
    read_text — 재입력 루프 포함)
  - `view/{main,sample,order,approval,monitoring,production,shipment}_view.py`
  - `controller/{main,sample,order,approval,monitoring,production,shipment}_controller.py`
    (Cycle 1~7에서 TDD로 검증된 서비스/저장소를 호출하는 배선)
  - `src/sample_order_system/main.py`(CLI 진입점, --db 인자), 루트 `main.py`(src 경로 부트스트랩)
- **자동화 검증**: 전체 스위트(`pytest`) → 37 passed. `ruff check src tests main.py` →
  All checks passed.
- **수동 검증(골든 패스, 임시 DB로 실행)**:
  1. 시료 등록(S-001, 재고 10) → 시료 주문(수량 30, 재고부족) → 승인(Y) → `PRODUCING` 전환,
     생산 큐에 부족분 20/실생산량 22/총생산시간 11.0분 작업 등록 확인
  2. 생산라인 조회 → 현재 작업 표시 확인 → 생산완료 처리 → 재고 10→2(=10+22-30) 반영 확인,
     주문 `CONFIRMED` 전환 확인
  3. 모니터링(주문량 확인/재고량 확인) → CONFIRMED 1건, 재고 2/대기수요 0/여유/100% 정상 출력
  4. 출고 처리 → 주문 `RELEASE` 전환 확인, 메인 메뉴 종료(`0`) → 정상 종료(트레이스백 없음)
  5. 잘못된 입력(`abc`, `9`, `xyz`) 시도 → 프로그램이 죽지 않고 "다시 입력해주세요" 재입력
     요구 확인 (PRD.md 7절의 "입력값 검증 부족" PoC 갭 해소 확인)
  6. 동일 DB로 재실행 → 이전에 등록한 시료가 그대로 조회됨 → 영속성 확인
- **상태**: 완료. REVIEW 단계로 진행 예정 (커밋 없음).

### Cycle 8 — REVIEW

- **스코프 검토**: Plan.md 범위를 벗어난 신규 비즈니스 로직 없음.
- **리팩토링 발견 및 승인**: `approval_view.py`/`shipment_view.py`의 번호 범위 검증과 주문
  목록 출력 형식이 중복 → 사람 파트너에게 제안 후 **"지금 진행"** 승인받아 즉시 수행.
  - `view/prompts.py`에 `read_index_in_range(prompt, count)` 추가
  - `view/order_list_view.py` 신규(`show_order_list(orders, empty_message)`)
  - `approval_view.py`, `shipment_view.py`가 위 공통 헬퍼를 사용하도록 축약
- **REVIEW 후 재검증**: 전체 테스트 37 passed 유지, `ruff check` All checks passed.
  리팩토링 이후 승인→출고 콘솔 흐름을 다시 수동 실행해 정상 동작 재확인.
- **커밋 시점 2 대기 중**: GREEN+REVIEW 전체(view/, controller/, main.py, src의
  sample_order_system/main.py, 관련 테스트) + Plan.md `[Cycle 8][GREEN+REVIEW]` 커밋&푸쉬
  승인 대기.

## 이력 (History)

### [2026-07-15] Cycle 0 — 아키텍처 스캐폴딩 + pytest 하네스 구성 완료

- **목표**: 이후 TDD 사이클(1~8)이 코드를 놓을 수 있는 최소 골격 마련. 프로덕션 로직 미포함.
- **TDD 예외 근거**: SKILL.md의 "예외: 설정(configuration) 파일"에 해당하는 순수 스캐폴딩이며,
  사용자가 "Cycle 0 진행하자"로 승인. 실패 테스트 없이 진행.
- **수행 내용**:
  - `src/sample_order_system/{model,repository,service,view,controller}/__init__.py` 골격 생성
  - `tests/__init__.py`, `tests/conftest.py`(임시 SQLite 경로 픽스처 `tmp_db_path`) 생성
  - `pyproject.toml`(`[tool.pytest.ini_options]` pythonpath=src, testpaths=tests / `[tool.ruff]`)
  - `requirements-dev.txt` (pytest, ruff)
  - 기존 `.gitignore`(`/.venv/`, `/.idea`)에 `__pycache__/`, `*.pyc`, `.pytest_cache/`,
    `.ruff_cache/`, `*.db` 추가
  - `COMMIT_CONVENTION.md`에 TDD 예외용 `SETUP` 커밋 유형 추가
  - 검증: `pytest --collect-only` → 0 tests collected(예상된 정상 상태, exit 5),
    `ruff check src tests` → All checks passed
- **상태**: 완료. 커밋(`[Cycle 0][SETUP]`) 실행은 사람 파트너 승인 대기 중.
- **다음 액션 후보**: 사용자 커밋 승인 → Cycle 1(Sample 모델/Repository) RED 단계 Plan 작성.

### [2026-07-15] 설계 결정 확정 반영 (PRD.md 갱신)

- **배경**: 직전 이력 항목에서 사용자에게 확인 요청한 4가지 미해결 사항에 대한 답변 확정.
- **확정된 결정**:
  1. 재고 차감 시점 → **주문 승인(CONFIRMED 전환) 시점**에 즉시 차감. 생산이 필요했던 경우는
     생산완료로 재고가 채워진 뒤 그 시점에 차감.
  2. 생산완료 트리거 → **담당자가 생산라인 메뉴에서 수동으로 "생산완료 처리"**.
  3. PoC 처리 방침 → **`PoC/`는 그대로 보존(참고 자료), 최종 구현은 `src/` 아래 신규 작성**.
  4. 의존성 정책 → **런타임은 표준 라이브러리만, pytest/ruff 등 개발 도구는 허용**.
- **수행 내용**: 위 결정을 `PRD.md`(4.4/4.6/6/7절)와 `CLAUDE.md`(디렉토리 구조/의존성 절)에 반영.
- **상태**: 완료.
- **다음 액션 후보**: 아키텍처 스캐폴딩(디렉토리 구조, pytest 하네스, conftest 픽스처) 계획을
  세워 승인받고 TDD 사이클 1(시료 등록) RED 단계로 진입.

### [2026-07-15] Agentic Engineering 개발 계획 수립 및 문서 체계 초안 작성

- **배경**: `mission.png`의 주안점(① CLAUDE.md/PRD.md 등 문서 관리, ② Harness 도입, ③ Test,
  ④ CleanCode, ⑤ Commit 이력)과 `.claude/skills/test-driven-development/SKILL.md`의
  RED → GREEN → REVIEW 휴먼인더루프 워크플로우를 결합하여 전체 개발 계획을 수립.
- **수행 내용**:
  - `CLAUDE.md` 신규 작성 — 프로젝트 규칙, 아키텍처 방향, Agentic Engineering 워크플로우 안내
  - `PRD.md` 신규 작성 — `system.pdf` 기능명세 + PoC 4종 코드 리뷰에서 발견된 갭을 반영한
    최종 요구사항 정리, 미해결 설계 결정 사항 명시
  - `COMMIT_CONVENTION.md` 신규 작성 — SKILL.md가 참조하지만 실제 파일이 없어 새로 정의
  - `Plan.md`(본 문서) 신규 작성 — 액션 기록/이력 관리 체계 확립
  - 사용자에게 미해결 설계 결정 사항(재고 차감 시점, 생산완료 트리거 방식, 기존 PoC 코드 처리
    방침, 개발 의존성 정책) 확인 질문 전달
- **상태**: 완료. 단, PRD.md 내 일부 항목은 사용자 확인 후 확정 예정(`TBD` 표기).
- **다음 액션 후보**: 사용자 답변을 반영해 PRD.md 확정 → 아키텍처 스캐폴딩(디렉토리 구조,
  테스트 하네스 세팅)에 대한 Plan 작성 및 승인 요청 → TDD 사이클 1 시작(RED).
