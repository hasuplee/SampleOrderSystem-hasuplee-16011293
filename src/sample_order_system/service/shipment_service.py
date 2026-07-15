from sample_order_system.model.order import OrderStatus
from sample_order_system.repository.order_repository import OrderRepository


class ShipmentService:
    """CONFIRMED 주문의 출고 처리를 담당."""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def release_order(self, order_id: str) -> None:
        order = self.order_repository.get(order_id)
        if order is None:
            raise ValueError(f"존재하지 않는 주문입니다: {order_id}")
        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(
                f"CONFIRMED 상태의 주문만 출고 처리할 수 있습니다: {order_id} ({order.status.value})"
            )

        order.status = OrderStatus.RELEASE
        self.order_repository.update(order)
