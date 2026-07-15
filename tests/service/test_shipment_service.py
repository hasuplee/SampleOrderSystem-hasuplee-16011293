import pytest

from sample_order_system.model.order import OrderStatus
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.production_job_repository import ProductionJobRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.approval_service import ApprovalService
from sample_order_system.service.order_service import OrderService
from sample_order_system.service.shipment_service import ShipmentService


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


def test_CONFIRMED_주문을_출고처리하면_RELEASE_상태로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    ApprovalService(
        sample_repo, order_repo, ProductionQueue(), ProductionJobRepository(tmp_db_path),
    ).approve_order(order.order_id)
    service = ShipmentService(order_repo)

    service.release_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.RELEASE


def test_존재하지_않는_주문을_출고처리하면_예외가_발생한다(tmp_db_path):
    _, order_repo, _ = _주문_준비(tmp_db_path)
    service = ShipmentService(order_repo)

    with pytest.raises(ValueError):
        service.release_order("ORD-NOT-EXIST")


def test_CONFIRMED가_아닌_주문을_출고처리하면_예외가_발생한다(tmp_db_path):
    _, order_repo, order = _주문_준비(tmp_db_path)
    service = ShipmentService(order_repo)

    with pytest.raises(ValueError):
        service.release_order(order.order_id)
