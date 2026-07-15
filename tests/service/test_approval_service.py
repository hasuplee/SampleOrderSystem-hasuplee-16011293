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


def _주문_준비(tmp_db_path, stock=100, quantity=30, avg_production_time=0.5, yield_rate=0.92):
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
    return sample_repo, order_repo, order


def _서비스(tmp_db_path, sample_repo, order_repo, production_queue=None):
    return ApprovalService(
        sample_repo,
        order_repo,
        production_queue or ProductionQueue(),
        ProductionJobRepository(tmp_db_path),
    )


def test_주문을_거절하면_REJECTED_상태로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    service.reject_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.REJECTED


def test_재고가_충분하면_승인시_CONFIRMED_상태로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    service.approve_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.CONFIRMED


def test_재고가_충분하면_승인시_재고가_주문수량만큼_차감된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    service.approve_order(order.order_id)

    assert sample_repo.get("S-001").stock == 70


def test_재고가_부족하면_승인시_생산_큐에_작업이_등록된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(
        tmp_db_path, stock=10, quantity=30, avg_production_time=0.5, yield_rate=0.92,
    )
    queue = ProductionQueue()
    service = _서비스(tmp_db_path, sample_repo, order_repo, queue)

    service.approve_order(order.order_id)

    job = queue.dequeue()
    shortage = 20
    actual_qty = math.ceil(shortage / 0.92)
    assert job.order_id == order.order_id
    assert job.sample_id == "S-001"
    assert job.shortage_qty == shortage
    assert job.actual_qty == actual_qty
    assert job.total_time_min == pytest.approx(0.5 * actual_qty)


def test_재고가_부족하면_승인시_생산_작업이_저장소에도_기록된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(
        tmp_db_path, stock=10, quantity=30, avg_production_time=0.5, yield_rate=0.92,
    )
    job_repo = ProductionJobRepository(tmp_db_path)
    service = ApprovalService(sample_repo, order_repo, ProductionQueue(), job_repo)

    service.approve_order(order.order_id)

    stored = job_repo.list_all()
    assert len(stored) == 1
    assert stored[0].order_id == order.order_id
    assert stored[0].actual_qty == math.ceil(20 / 0.92)


def test_재고가_부족하면_승인시_주문_상태가_PRODUCING으로_변경된다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=10, quantity=30)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    service.approve_order(order.order_id)

    assert order_repo.get(order.order_id).status == OrderStatus.PRODUCING


def test_재고가_충분하면_미리보기는_sufficient가_True다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(tmp_db_path, stock=100, quantity=30)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    preview = service.preview_approval(order.order_id)

    assert preview.sufficient is True
    assert sample_repo.get("S-001").stock == 100
    assert order_repo.get(order.order_id).status == OrderStatus.RESERVED


def test_재고가_부족하면_미리보기에_부족분과_실생산량이_계산되어_있다(tmp_db_path):
    sample_repo, order_repo, order = _주문_준비(
        tmp_db_path, stock=10, quantity=30, avg_production_time=0.5, yield_rate=0.92,
    )
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    preview = service.preview_approval(order.order_id)

    shortage = 20
    actual_qty = math.ceil(shortage / 0.92)
    assert preview.sufficient is False
    assert preview.shortage_qty == shortage
    assert preview.actual_qty == actual_qty
    assert preview.total_time_min == pytest.approx(0.5 * actual_qty)
    assert sample_repo.get("S-001").stock == 10
    assert order_repo.get(order.order_id).status == OrderStatus.RESERVED


def test_존재하지_않는_주문을_승인하면_예외가_발생한다(tmp_db_path):
    sample_repo, order_repo, _ = _주문_준비(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    with pytest.raises(ValueError):
        service.approve_order("ORD-NOT-EXIST")


def test_존재하지_않는_주문을_거절하면_예외가_발생한다(tmp_db_path):
    sample_repo, order_repo, _ = _주문_준비(tmp_db_path)
    service = _서비스(tmp_db_path, sample_repo, order_repo)

    with pytest.raises(ValueError):
        service.reject_order("ORD-NOT-EXIST")
