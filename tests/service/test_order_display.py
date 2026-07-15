from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.order_display import resolve_sample_names
from sample_order_system.service.order_service import OrderService


def test_주문_목록을_변환하면_시료명이_포함된다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    sample_repo.create(Sample(
        sample_id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=100,
    ))
    order_repo = OrderRepository(tmp_db_path)
    order = OrderService(sample_repo, order_repo).create_order(
        sample_id="S-001", customer_name="삼성전자 파운드리", quantity=200,
    )

    rows = resolve_sample_names([order], sample_repo)

    assert rows == [{
        "order_id": order.order_id,
        "customer_name": "삼성전자 파운드리",
        "sample_name": "실리콘 웨이퍼-8인치",
        "quantity": 200,
    }]
