import pytest

from sample_order_system.model.order import OrderStatus
from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.approval_service import ApprovalService
from sample_order_system.service.order_service import OrderService


def _주문_준비(tmp_db_path, stock=100, quantity=30):
    sample_repo = SampleRepository(tmp_db_path)
    sample_repo.create(Sample(
        sample_id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=stock,
    ))
    order_repo = OrderRepository(tmp_db_path)
    order = OrderService(sample_repo, order_repo).create_order(
        sample_id="S-001", customer_name="삼성전자 파운드리", quantity=quantity,
    )
    return sample_repo, order_repo, order


def test_주문을_거절하면_REJECTED_상태로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path)
    service = ApprovalService(sample_repo, order_repo)

    service.reject_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.REJECTED


def test_재고가_충분하면_승인시_CONFIRMED_상태로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    service = ApprovalService(sample_repo, order_repo)

    service.approve_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.CONFIRMED


def test_재고가_충분하면_승인시_재고가_주문수량만큼_차감된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    service = ApprovalService(sample_repo, order_repo)

    service.approve_order(order.order_id)

    assert sample_repo.get("S-001").stock == 70


def test_재고가_부족하면_승인시_NotImplementedError가_발생한다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=10, quantity=30)
    service = ApprovalService(sample_repo, order_repo)

    with pytest.raises(NotImplementedError):
        service.approve_order(order.order_id)
