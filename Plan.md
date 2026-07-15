# Plan.md

이 문서는 SampleOrderSystem 프로젝트에서 수행되는 모든 액션(설계·문서화·구현·리팩터링 등)을
**실행 전에 먼저 기록**하고, 실행 후 결과를 이력으로 남기기 위한 문서입니다.

- 기능 구현에 관한 세부 RED/GREEN/REVIEW 계획은 `.claude/skills/test-driven-development/SKILL.md` 규칙을 따르며,
  해당 문서가 요구하는 Plan(목표/범위/테스트 계획)도 이 파일에 사이클 단위로 기록합니다.
- 그 외 모든 액션(문서 작성, 아키텍처 결정, 리팩터링 제안 등)도 실행 전 "진행 중" 항목으로 먼저 적고,
  완료되면 "이력"으로 이동시킵니다.
- 커밋은 사람 파트너의 명시적 확인 없이 실행하지 않습니다 (SKILL.md 준수).

## 진행 중 (Active)

_현재 진행 중인 액션 없음. Cycle 0 완료, 커밋 승인 대기 중._

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
