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
   초기 재고를 입력해 시료를 등록합니다.
2. **[2] 시료 주문**: 등록한 시료 ID로 고객명·수량을 입력해 주문을 생성합니다
   (상태: `RESERVED`).
3. **[3] 주문 승인/거절**: 대기 중인 주문을 선택해 승인(Y) 또는 거절(N) 처리합니다.
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

## 테스트 실행

```bash
pytest            # 전체 테스트
pytest -v         # 상세 출력
pytest tests/service/test_order_service.py -v   # 특정 파일만
```

## 린트

```bash
ruff check src tests main.py
```

## 프로젝트 구조

```
SampleOrderSystem/
├── main.py                          # 실행 진입점 (src 경로 부트스트랩)
├── src/sample_order_system/
│   ├── main.py                      # 실제 진입점 (CLI 인자 파싱, 서비스 조립)
│   ├── model/                       # Sample, Order, ProductionJob/Queue 등 데이터 모델
│   ├── db/                          # SQLite 연결 및 스키마 초기화
│   ├── repository/                  # Sample/Order CRUD (SQLite)
│   ├── service/                     # 주문/승인/생산/출고/모니터링 도메인 로직
│   ├── view/                        # 콘솔 입출력 (비즈니스 로직 없음)
│   └── controller/                  # 메뉴 흐름 제어
├── tests/                           # pytest 테스트 (src와 대응하는 구조)
├── PoC/                              # 개발 초기 프로토타입(참고용, 최종 구현에 미사용)
├── PRD.md / CLAUDE.md / Plan.md / COMMIT_CONVENTION.md   # 문서 관리
└── requirements-dev.txt             # 개발 의존성 (pytest, ruff)
```

## 데이터 영속성

시료(Sample)·주문(Order) 데이터는 SQLite 파일에 저장되어 프로그램을 재실행해도 유지됩니다.
생산 큐(ProductionQueue)는 콘솔 세션 동안만 메모리에 유지되며, 프로그램을 종료하면
초기화됩니다(알려진 제한 사항, `PRD.md` 참고).
