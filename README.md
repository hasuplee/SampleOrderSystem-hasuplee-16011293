# 반도체 시료 생산주문관리 시스템 (SampleOrderSystem)

가상의 반도체 회사 "S-Semi"의 시료(Sample) 생산·주문 관리를 위한 콘솔 프로그램입니다.
고객 주문 접수 → 승인/거절 → (재고 부족 시) 생산 → 출고로 이어지는 흐름을 콘솔 메뉴로 제공합니다.

상세 기능 명세는 [`PRD.md`](./PRD.md), 개발 규칙/아키텍처는 [`CLAUDE.md`](./CLAUDE.md),
개발 진행 이력은 [`Plan.md`](./Plan.md)를 참고하세요.

## 요구 사항

- Python 3.10 이상 (표준 라이브러리만으로 실행 가능)
- 테스트/린트를 실행하려면 개발 의존성 설치 필요: `pytest`, `ruff`

## 설치

```bash
git clone https://github.com/hasuplee/SampleOrderSystem-hasuplee-16011293.git
cd SampleOrderSystem-hasuplee-16011293

# 테스트/린트를 실행할 경우에만 필요 (런타임 실행에는 불필요)
pip install -r requirements-dev.txt
```

## 실행 방법

프로젝트 루트에서 `main.py`를 실행합니다.

```bash
python main.py
```

기본적으로 현재 디렉터리의 `sample_order.db`(SQLite)에 데이터가 저장되며, 프로그램을
다시 실행해도 이전 데이터가 유지됩니다. DB 파일 경로는 `--db` 옵션으로 바꿀 수 있습니다.

```bash
python main.py --db path/to/other.db
```

Windows 콘솔에서 한글이 깨지면 아래처럼 UTF-8 코드페이지로 전환한 뒤 실행하세요.

```powershell
chcp 65001
python main.py
```

### 메인 메뉴

```
[1] 시료 관리        [2] 시료 주문
[3] 주문 승인/거절   [4] 모니터링
[5] 생산라인 조회    [6] 출고 처리
[0] 종료
```

### 기본 사용 흐름 (권장 순서)

처음 실행 시 등록된 시료가 없으므로, 아래 순서로 진행하면 전체 흐름을 확인할 수 있습니다.

1. **[1] 시료 관리 → 시료 등록**: 시료 ID, 이름, 평균 생산시간(min/ea), 수율(0.0~1.0),
   초기 재고를 입력해 시료를 등록합니다. 수율은 0 초과 1.0 이하, 평균 생산시간은 0보다
   커야 하며, 범위를 벗어나면 등록이 거부됩니다.
2. **[2] 시료 주문**: 등록한 시료 ID로 고객명·수량을 입력해 주문을 생성합니다
   (상태: `RESERVED`).
3. **[3] 주문 승인/거절**: 대기 중인 주문을 선택하면 먼저 재고 확인 결과(재고 충분
   여부, 부족 시 부족분/실생산량/총생산시간)를 보여준 뒤 승인(Y) 또는 거절(N)을
   묻습니다.
   - 재고가 충분하면 주문 수량만큼 재고가 차감되고 즉시 `CONFIRMED`로 전환됩니다.
   - 재고가 부족하면 부족분에 대한 생산 작업이 생산 큐에 등록되고 주문은 `PRODUCING`으로
     전환됩니다.
4. **[5] 생산라인 조회**: 현재 생산 중인 작업과 대기 큐를 확인하고, 필요 시
   **생산완료 처리**를 실행합니다. 완료 처리 시 재고가 실생산량만큼 증가한 뒤 주문
   수량만큼 차감되고, 주문이 `CONFIRMED`로 전환됩니다.
5. **[4] 모니터링**: 상태별 주문 건수와 시료별 재고 현황(여유/부족/고갈)을 확인합니다.
6. **[6] 출고 처리**: `CONFIRMED` 상태인 주문을 선택해 `RELEASE` 처리합니다.

잘못된 값(문자, 범위 밖 번호 등)을 입력하면 프로그램이 종료되지 않고 다시 입력하라는
안내가 표시됩니다.

## 예시 DB로 재현해보기

`examples/` 폴더에는 `system.pdf`에 실린 예시 화면(1~6번)과 동일한 데이터를 담은
SQLite DB(`example.db`)와 이를 생성하는 시드 스크립트(`seed_example_db.py`)가 있습니다.

```bash
python main.py --db examples/example.db
```

시딩된 데이터:

- 시료 12종 (`S-001`~`S-005`는 예시 이미지와 동일 값, `S-006`~`S-012`는 "12종"이라는
  개수만 언급되고 세부값이 없어 임의로 채운 값)
- 주문 4건
  - `ORD-0001` LG이노텍 / 산화막 웨이퍼-SiO2 / 300 ea → `RESERVED`
  - `ORD-0002` SK하이닉스 / 실리콘 웨이퍼-8인치 / 150 ea → `RESERVED`
  - `ORD-0003` 삼성전자 파운드리 / SiC 파워기판-6인치 / 200 ea → `RESERVED`
  - `ORD-0004` DB하이텍 / 포토레지스트-PR7 / 400 ea → 이미 승인되어 `CONFIRMED`
    (출고 처리를 바로 시연할 수 있도록 미리 처리해 둠)

메인 메뉴에서 아래 순서로 입력하면 예시 이미지의 각 장면을 그대로 재현할 수 있습니다.

| 메뉴 입력 | 재현되는 장면 |
|---|---|
| `1` → `2` | 시료 목록 (이미지 1) |
| `0` → `3` → `3` → `Y` | 승인/거절 — 3번(SiC, 삼성전자 파운드리) 선택 시 재고 확인 미리보기(부족분/실생산량/총생산시간)가 먼저 표시된 뒤, 승인하면 재고 부족으로 `PRODUCING` 전환 (이미지 3). 수치는 `ceil(부족분/수율)` 공식대로 정확히 계산되어 이미지의 예시 수치(목업)와는 다를 수 있음 |
| `5` → `1` | 생산라인 조회 → 생산완료 처리 (이미지 5) |
| `4` → `1` (또는 `2`) → `0` | 모니터링 — 상태별 주문 건수 / 재고 현황 (이미지 4) |
| `6` → `1` | 출고 처리 — 목록에 뜬 `CONFIRMED` 주문 중 하나를 선택해 `RELEASE` (이미지 6) |
| `0` | 종료 |

DB를 초기 상태로 되돌리려면 시드 스크립트를 다시 실행하세요(기존 `example.db`를 지우고
새로 만듭니다).

```bash
python examples/seed_example_db.py
```

## 테스트 실행

```bash
pytest            # 전체 테스트
pytest -v         # 상세 출력
pytest tests/service/test_order_service.py -v   # 특정 파일만
```

## 린트

```bash
ruff check src tests main.py examples/seed_example_db.py
```

## 프로젝트 구조

```
SampleOrderSystem/
├── main.py                          # 실행 진입점 (src 경로 부트스트랩)
├── src/sample_order_system/
│   ├── main.py                      # 실제 진입점 (CLI 인자 파싱, 서비스 조립)
│   ├── model/                       # Sample, Order, ProductionJob/Queue, ApprovalPreview 등
│   ├── db/                          # SQLite 연결 및 스키마 초기화
│   ├── repository/                  # Sample/Order/ProductionJob CRUD (SQLite)
│   ├── service/                     # 주문/승인/생산/출고/모니터링 도메인 로직
│   ├── view/                        # 콘솔 입출력 (비즈니스 로직 없음)
│   └── controller/                  # 메뉴 흐름 제어
├── tests/                           # pytest 테스트 (src와 대응하는 구조)
├── examples/                        # 예시 DB 시드 스크립트 + example.db ("예시 DB로 재현해보기" 참고)
├── PRD.md / CLAUDE.md / Plan.md / COMMIT_CONVENTION.md   # 문서 관리
└── requirements-dev.txt             # 개발 의존성 (pytest, ruff)
```

> `PoC/`(개발 초기 프로토타입)는 로컬 작업 폴더에는 있지만 `.gitignore`(`/PoC`)로
> 제외되어 있어 저장소에는 포함되지 않습니다. 클론한 저장소에는 존재하지 않습니다.

## 데이터 영속성

시료(Sample)·주문(Order)·생산 작업(ProductionJob) 데이터는 모두 SQLite 파일에 저장되어
프로그램을 재실행해도 유지됩니다. 재고 부족으로 생산 큐에 등록된 작업은 `production_jobs`
테이블에도 함께 기록되며, 프로그램을 재시작하면 남아있는 작업이 자동으로 큐에 복원되어
이전 세션에서 `PRODUCING` 상태로 남은 주문도 이어서 생산완료 처리할 수 있습니다.
