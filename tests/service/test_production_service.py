import math

import pytest

from sample_order_system.model.order import OrderStatus
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.production_job_repository import ProductionJobRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.approval_service import ApprovalService
from sample_order_system.service.order_service import OrderService
from sample_order_system.service.production_service import ProductionService


def _생산중인_주문_준비(tmp_db_path, stock=10, quantity=30, avg_production_time=0.5, yield_rate=0.92):
    sample_repo = SampleRepository(tmp_db_path)
    sample_repo.create(Sample(
        sample_id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=avg_production_time,
        yield_rate=yield_rate,
        stock=stock,
    ))
    order_repo = OrderRepository(tmp_db_path)
    order = OrderService(sample_repo, order_repo).create_order(
        sample_id="S-001", customer_name="삼성전자 파운드리", quantity=quantity,
    )
    queue = ProductionQueue()
    job_repo = ProductionJobRepository(tmp_db_path)
    ApprovalService(sample_repo, order_repo, queue, job_repo).approve_order(order.order_id)
    return sample_repo, order_repo, queue, order


def test_생산완료_처리하면_재고가_실생산량만큼_증가한_뒤_주문수량만큼_차감된다(tmp_db_path):
    sample_repo, order_repo, queue, order = _생산중인_주문_준비(
        tmp_db_path, stock=10, quantity=30, avg_production_time=0.5, yield_rate=0.92,
    )
    service = ProductionService(sample_repo, order_repo, queue)

    service.complete_current_job()

    shortage = 20
    actual_qty = math.ceil(shortage / 0.92)
    expected_stock = 10 + actual_qty - 30
    assert sample_repo.get("S-001").stock == expected_stock


def test_생산완료_처리하면_주문_상태가_CONFIRMED로_변경된다(tmp_db_path):
    sample_repo, order_repo, queue, order = _생산중인_주문_준비(tmp_db_path)
    service = ProductionService(sample_repo, order_repo, queue)

    service.complete_current_job()

    assert order_repo.get(order.order_id).status == OrderStatus.CONFIRMED


def test_생산완료_처리하면_생산_큐에서_작업이_제거된다(tmp_db_path):
    sample_repo, order_repo, queue, order = _생산중인_주문_준비(tmp_db_path)
    service = ProductionService(sample_repo, order_repo, queue)

    service.complete_current_job()

    assert queue.peek() is None


def test_생산_큐가_비어있으면_생산완료_처리시_예외가_발생한다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    order_repo = OrderRepository(tmp_db_path)
    queue = ProductionQueue()
    service = ProductionService(sample_repo, order_repo, queue)

    with pytest.raises(ValueError):
        service.complete_current_job()
