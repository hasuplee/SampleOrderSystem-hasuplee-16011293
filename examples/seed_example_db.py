"""examples/1~6.png 예시 화면을 재현하기 위한 시드 데이터 생성 스크립트.

실행:
    python examples/seed_example_db.py

생성 결과 (examples/example.db):
- 시료 12종 (S-001~S-005는 예시 이미지와 동일 값, S-006~S-012는 "12종" 개수를 맞추기
  위해 임의로 채운 값 — 이미지에 세부값이 없음)
- 주문 4건
  - ORD-0001 LG이노텍 / 산화막 웨이퍼-SiO2(S-005) / 300 ea → RESERVED (직접 승인해보세요)
  - ORD-0002 SK하이닉스 / 실리콘 웨이퍼-8인치(S-001) / 150 ea → RESERVED (재고 충분 승인 예시)
  - ORD-0003 삼성전자 파운드리 / SiC 파워기판-6인치(S-003) / 200 ea → RESERVED (재고 부족 승인 예시)
  - ORD-0004 DB하이텍 / 포토레지스트-PR7(S-004) / 400 ea → 스크립트가 미리 승인해 CONFIRMED
    (출고 처리를 바로 시연할 수 있도록)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sample_order_system.model.production_queue import ProductionQueue  # noqa: E402
from sample_order_system.model.sample import Sample  # noqa: E402
from sample_order_system.repository.order_repository import OrderRepository  # noqa: E402
from sample_order_system.repository.production_job_repository import (  # noqa: E402
    ProductionJobRepository,
)
from sample_order_system.repository.sample_repository import SampleRepository  # noqa: E402
from sample_order_system.service.approval_service import ApprovalService  # noqa: E402
from sample_order_system.service.order_service import OrderService  # noqa: E402

DB_PATH = Path(__file__).resolve().parent / "example.db"

SAMPLES = [
    # sample_id, name, avg_production_time, yield_rate, stock
    ("S-001", "실리콘 웨이퍼-8인치", 0.5, 0.92, 480),
    ("S-002", "GaN 에피택셜-4인치", 0.3, 0.78, 220),
    ("S-003", "SiC 파워기판-6인치", 0.8, 0.92, 30),
    ("S-004", "포토레지스트-PR7", 0.2, 0.95, 910),
    ("S-005", "산화막 웨이퍼-SiO2", 0.6, 0.88, 0),
    ("S-006", "게르마늄 기판-4인치", 0.4, 0.85, 150),
    ("S-007", "사파이어 기판-2인치", 0.7, 0.80, 60),
    ("S-008", "질화붕소 박막-A", 0.3, 0.90, 300),
    ("S-009", "실리콘 웨이퍼-12인치", 0.9, 0.90, 40),
    ("S-010", "GaN 에피택셜-6인치", 0.5, 0.82, 75),
    ("S-011", "포토레지스트-PR9", 0.25, 0.93, 500),
    ("S-012", "산화막 웨이퍼-SiO2-B", 0.6, 0.87, 20),
]

ORDERS = [
    # sample_id, customer_name, quantity
    ("S-005", "LG이노텍", 300),
    ("S-001", "SK하이닉스", 150),
    ("S-003", "삼성전자 파운드리", 200),
    ("S-004", "DB하이텍", 400),
]


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    sample_repository = SampleRepository(DB_PATH)
    order_repository = OrderRepository(DB_PATH)
    order_service = OrderService(sample_repository, order_repository)
    approval_service = ApprovalService(
        sample_repository, order_repository, ProductionQueue(),
        ProductionJobRepository(DB_PATH),
    )

    for sample_id, name, avg_production_time, yield_rate, stock in SAMPLES:
        sample_repository.create(Sample(
            sample_id=sample_id,
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
            stock=stock,
        ))

    created = [
        order_service.create_order(sample_id=sid, customer_name=name, quantity=qty)
        for sid, name, qty in ORDERS
    ]

    # DB하이텍/포토레지스트 주문은 미리 승인해 CONFIRMED로 만들어 출고 처리를 바로 시연 가능하게 함
    approval_service.approve_order(created[-1].order_id)

    print(f"생성 완료: {DB_PATH}")
    print(f"시료 {len(SAMPLES)}종, 주문 {len(ORDERS)}건 (그중 1건은 CONFIRMED로 미리 승인됨)")


if __name__ == "__main__":
    main()
