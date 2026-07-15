import pytest

from sample_order_system.model.order import OrderStatus
from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.order_service import OrderService


def _시료_등록(tmp_db_path, sample_id="S-001"):
    sample_repo = SampleRepository(tmp_db_path)
    sample_repo.create(Sample(
        sample_id=sample_id,
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=100,
    ))
    return sample_repo


def _서비스(tmp_db_path, sample_repo):
    return OrderService(sample_repo, OrderRepository(tmp_db_path))


def test_등록된_시료로_주문하면_RESERVED_상태로_생성된다(tmp_db_path):
    sample_repo = _시료_등록(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo)

    order = service.create_order(sample_id="S-001", customer_name="삼성전자 파운드리", quantity=200)

    assert order.sample_id == "S-001"
    assert order.customer_name == "삼성전자 파운드리"
    assert order.quantity == 200
    assert order.status == OrderStatus.RESERVED


def test_등록되지_않은_시료_ID로_주문하면_예외가_발생한다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo)

    with pytest.raises(ValueError):
        service.create_order(sample_id="S-NOT-EXIST", customer_name="LG이노텍", quantity=10)


def test_주문_ID는_ORD_형식으로_순차_채번된다(tmp_db_path):
    sample_repo = _시료_등록(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo)

    first = service.create_order(sample_id="S-001", customer_name="SK하이닉스", quantity=50)
    second = service.create_order(sample_id="S-001", customer_name="DB하이텍", quantity=30)

    assert first.order_id == "ORD-0001"
    assert second.order_id == "ORD-0002"
