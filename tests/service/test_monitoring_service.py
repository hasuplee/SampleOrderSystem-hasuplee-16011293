from sample_order_system.model.order import OrderStatus
from sample_order_system.model.sample import Sample
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.monitoring_service import MonitoringService
from sample_order_system.service.order_service import OrderService


def _시료_등록(sample_repo, sample_id="S-001", stock=100):
    sample_repo.create(Sample(
        sample_id=sample_id,
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=stock,
    ))


def _주문_생성(sample_repo, order_repo, sample_id="S-001", quantity=30, status=None):
    order = OrderService(sample_repo, order_repo).create_order(
        sample_id=sample_id, customer_name="삼성전자 파운드리", quantity=quantity,
    )
    if status is not None:
        order.status = status
        order_repo.update(order)
    return order


def test_상태별_주문_건수를_집계할_수_있다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    order_repo = OrderRepository(tmp_db_path)
    _시료_등록(sample_repo)
    _주문_생성(sample_repo, order_repo, status=OrderStatus.RESERVED)
    _주문_생성(sample_repo, order_repo, status=OrderStatus.CONFIRMED)
    _주문_생성(sample_repo, order_repo, status=OrderStatus.PRODUCING)
    _주문_생성(sample_repo, order_repo, status=OrderStatus.RELEASE)
    _주문_생성(sample_repo, order_repo, status=OrderStatus.REJECTED)

    counts = MonitoringService(sample_repo, order_repo).status_counts()

    assert counts == {"RESERVED": 1, "CONFIRMED": 1, "PRODUCING": 1, "RELEASE": 1}


def test_재고가_0이면_고갈_상태이다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    order_repo = OrderRepository(tmp_db_path)
    _시료_등록(sample_repo, stock=0)
    _주문_생성(sample_repo, order_repo, quantity=10, status=OrderStatus.RESERVED)

    states = MonitoringService(sample_repo, order_repo).stock_states()

    assert states[0]["state"] == "고갈"


def test_재고가_대기수요보다_적으면_부족_상태이다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    order_repo = OrderRepository(tmp_db_path)
    _시료_등록(sample_repo, stock=5)
    _주문_생성(sample_repo, order_repo, quantity=10, status=OrderStatus.RESERVED)

    states = MonitoringService(sample_repo, order_repo).stock_states()

    assert states[0]["pending_demand"] == 10
    assert states[0]["state"] == "부족"


def test_재고가_대기수요_이상이면_여유_상태이다(tmp_db_path):
    sample_repo = SampleRepository(tmp_db_path)
    order_repo = OrderRepository(tmp_db_path)
    _시료_등록(sample_repo, stock=100)
    _주문_생성(sample_repo, order_repo, quantity=10, status=OrderStatus.RESERVED)

    states = MonitoringService(sample_repo, order_repo).stock_states()

    assert states[0]["state"] == "여유"
    assert states[0]["ratio"] == 1.0
