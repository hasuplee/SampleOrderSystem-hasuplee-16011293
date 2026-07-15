# COMMIT_CONVENTION.md

`.claude/skills/test-driven-development/SKILL.md`가 참조하는 커밋 메시지 규칙입니다.
커밋은 RED 종료 시점과 REVIEW 종료 시점, 단 두 곳에서만, 매번 사람 파트너의 명시적 승인 후에만 수행합니다.

## 사이클 번호

각 기능/버그수정 단위(TDD 한 바퀴)마다 `Plan.md`에 사이클 번호(N)를 부여하고,
해당 사이클의 두 커밋 모두 같은 번호를 사용합니다.

## 1) RED 종료 커밋

```
[Cycle N][RED] <기능/범위 요약>

- 목표: <Plan.md에 기록한 goal 한 줄 요약>
- 범위: <포함/제외 요약>
- 테스트: <실패 테스트 함수명 목록>
- 실패 확인: <pytest 실행 결과 요약, 예: "3 failed, 예상된 실패">
```

예:

```
[Cycle 3][RED] 시료 주문 시 존재하지 않는 시료 ID 거부

- 목표: 등록되지 않은 sample_id로 주문 생성 시 즉시 에러를 반환한다
- 범위: OrderController.create_order()만 대상. 재고 로직은 포함하지 않음
- 테스트: test_등록되지_않은_시료_ID로_주문하면_예외가_발생한다
- 실패 확인: 1 failed (기능 부재로 인한 예상된 실패)
```

## 2) REVIEW 종료 커밋

```
[Cycle N][GREEN+REVIEW] <기능/범위 요약>

- 구현: <핵심 변경 사항 요약>
- 리팩토링: <REVIEW 단계에서 승인받아 수행한 정리 내역, 없으면 "없음">
- 테스트: 전체 통과 (<pytest 요약, 예: "42 passed">)
```

예:

```
[Cycle 3][GREEN+REVIEW] 시료 주문 시 존재하지 않는 시료 ID 거부

- 구현: OrderController.create_order()에 sample_id 존재 검증 추가
- 리팩토링: 없음
- 테스트: 전체 통과 (18 passed)
```

## 3) SETUP 커밋 (TDD 예외 — 설정/스캐폴딩 전용)

SKILL.md의 TDD 예외 대상(설정 파일, 순수 스캐폴딩 등)으로 사람 파트너가 승인한 작업은
RED/GREEN 구분 없이 단일 커밋으로 처리한다.

```
[Cycle N][SETUP] <작업 요약>

- 내용: <추가/변경한 파일 요약>
- TDD 예외 근거: <Plan.md에 기록한 예외 사유 요약>
```

예:

```
[Cycle 0][SETUP] 아키텍처 스캐폴딩 + pytest 하네스 구성

- 내용: src/sample_order_system 패키지 골격, tests/ + pyproject.toml(pytest 설정),
  requirements-dev.txt, .gitignore 추가
- TDD 예외 근거: SKILL.md "설정 파일" 예외, 사람 파트너 승인(Plan.md Cycle 0 참고)
```

## 공통 규칙

- 제목은 72자 이내, 한글 요약 사용.
- 본문은 하이픈 목록 형식을 유지해 커밋 로그만으로 사이클의 목표→계획→구현→리뷰 흐름을
  재구성할 수 있게 합니다.
- `Co-Authored-By` 등 부가 트레일러는 harness 기본 규칙을 따릅니다.
