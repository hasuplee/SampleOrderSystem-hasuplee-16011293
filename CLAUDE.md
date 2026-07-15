# CLAUDE.md

이 저장소에서 작업하는 Claude Code(및 다른 에이전트)를 위한 프로젝트 규칙입니다.

## 프로젝트 개요

"반도체 시료 생산주문관리 시스템" 개인과제. 상세 기능 명세는 [`PRD.md`](./PRD.md)를 참고합니다.
`PoC/` 폴더에는 4개의 독립 프로토타입(ConsoleMVC, DataPersistence, DummyDataGenerator,
DataMonitor)이 존재하며, 최종 구현은 이들의 검증된 패턴(MVC 구조, SQLite Repository 패턴)을
계승하되 **PoC에서 발견된 갭(재고 미차감, 생산완료 메뉴 부재, 입력 검증 부족 등)을 반드시 해소**합니다.
갭 목록은 `PRD.md`의 "PoC 리뷰에서 발견된 갭" 절에 정리되어 있습니다.

## Agentic Engineering 워크플로우 (mission.png 주안점 반영)

이 프로젝트는 아래 5가지 주안점을 따라 진행합니다.

1. **문서 관리** — `CLAUDE.md`(본 문서, 규칙) / `PRD.md`(요구사항) / `Plan.md`(액션·계획 이력) /
   `COMMIT_CONVENTION.md`(커밋 규칙)을 항상 최신 상태로 유지합니다. 요구사항이나 설계가
   바뀌면 코드보다 먼저 해당 문서를 갱신합니다.
2. **Harness 도입** — pytest 기반 테스트 하네스, 재현 가능한 실행 환경(임시 SQLite DB 픽스처 등)을
   구성합니다. 구체적인 구성은 아키텍처 스캐폴딩 단계에서 `Plan.md`에 기록 후 진행합니다.
3. **Test** — 모든 기능 구현/버그 수정은 `.claude/skills/test-driven-development/SKILL.md`의
   RED → GREEN → REVIEW 사이클을 따릅니다 (아래 요약 참고).
4. **CleanCode** — 작은 함수, 명확한 이름, 불필요한 추상화·주석 지양. REVIEW 단계에서 점검합니다.
5. **Commit 이력** — 커밋은 RED 종료 시점과 REVIEW 종료 시점, 단 두 곳에서만, 그리고 매번
   사람 파트너의 명시적 승인을 받은 뒤에만 수행합니다. 메시지 형식은 `COMMIT_CONVENTION.md`를 따릅니다.
   **커밋 후에는 바로 `origin main`으로 푸쉬까지 수행합니다** (2026-07-15 사용자 지시로 "커밋"
   규칙이 "커밋&푸쉬"로 확장됨. 승인 시점·대상·횟수 등 기존 규칙은 동일하게 유지).

## 액션 전 Plan.md 기록 규칙 (필수)

**어떤 종류의 액션이든(문서 작성, 설계 결정, 코드 구현, 리팩터링, 커밋 등) 실행하기 전에
`Plan.md`에 먼저 기록**합니다.

- 기능 구현/버그수정 관련 액션: SKILL.md의 RED 단계 Plan(목표/범위/테스트 계획)을 `Plan.md`에
  작성 → 사람 파트너 승인 → 진행.
- 그 외 액션(문서화, 아키텍처 결정 등): 무엇을 할지 `Plan.md`의 "진행 중" 절에 먼저 적고 진행,
  완료 후 "이력" 절로 옮겨 결과를 기록합니다.
- `Plan.md`는 매 회 덮어쓰지 않고 이력이 누적되는 append-only 로그로 관리합니다.

## TDD 사이클 요약 (전체 규칙은 SKILL.md 참고)

```
RED    : 목표/범위/테스트 계획을 Plan.md에 작성 → 승인 → 실패 테스트 작성 → 실패 확인
         → [커밋 시점 1: 승인 후 Plan.md(+테스트) 커밋 & origin main 푸쉬]
GREEN  : Plan.md의 goal만 만족하는 최소 구현 → 테스트 통과 확인 (커밋 없음)
REVIEW : 스코프 크리프 점검, 리팩터링은 제안 후 승인받아 수행 → 테스트 그린 재확인
         → [커밋 시점 2: 승인 후 커밋 & origin main 푸쉬]
```

- 테스트 함수명은 `def test_한글...` 형식 (SKILL.md 네이밍 규칙).
- 커밋은 위 두 시점 외에는 제안하지도, 실행하지도 않습니다.

## 디렉토리 구조 (확정)

`PoC/`는 프로토타입 보관용으로 그대로 유지하고 수정하지 않습니다(참고 자료).
최종 구현은 아래처럼 `src/` 아래 신규 작성합니다(세부 하위 구조는 아키텍처 스캐폴딩 단계의
Plan.md 승인 시 확정).

```
src/
  sample_order_system/
    model/        # Sample, Order, ProductionJob 등 데이터 모델
    repository/    # SQLite 기반 CRUD (DataPersistence PoC 패턴 계승)
    service/       # 승인/거절, 생산, 출고 등 도메인 로직
    view/          # 콘솔 입출력 (비즈니스 로직 없음)
    controller/    # 메뉴 흐름 제어
tests/
  ...              # pytest 테스트, src와 대응하는 구조
```

## 의존성 정책 (확정)

- **런타임**: Python 표준 라이브러리만 사용(외부 패키지 의존성 없음, PoC 관례 계승).
- **개발 도구**: pytest, ruff 등 테스트·린트용 개발 의존성은 허용(런타임에는 포함되지 않음).

## 테스트 실행

```bash
pytest            # 전체 테스트
pytest -v         # 상세 출력
pytest path/to/test_file.py::test_이름   # 단일 테스트
```

## 참고 문서

- [`PRD.md`](./PRD.md) — 기능 요구사항, 데이터 모델, 미해결 설계 결정 사항
- [`Plan.md`](./Plan.md) — 액션 계획 및 이력 로그
- [`COMMIT_CONVENTION.md`](./COMMIT_CONVENTION.md) — 커밋 메시지 규칙
- [`.claude/skills/test-driven-development/SKILL.md`](./.claude/skills/test-driven-development/SKILL.md) — TDD 상세 규칙
