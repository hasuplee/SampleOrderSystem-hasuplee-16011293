from sample_order_system.model.order import Order, OrderStatus
from sample_order_system.repository.order_repository import OrderRepository


def test_생성된_주문을_조회하면_저장된_값과_동일하다(tmp_db_path):
    repo = OrderRepository(tmp_db_path)
    order = Order(
        order_id="ORD-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=200,
        status=OrderStatus.RESERVED,
    )

    repo.create(order)
    found = repo.get("ORD-0001")

    assert found == order


def test_주문_상태를_변경하면_저장된다(tmp_db_path):
    repo = OrderRepository(tmp_db_path)
    order = Order(
        order_id="ORD-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=200,
        status=OrderStatus.RESERVED,
    )
    repo.create(order)

    order.status = OrderStatus.CONFIRMED
    repo.update(order)

    assert repo.get("ORD-0001").status == OrderStatus.CONFIRMED
