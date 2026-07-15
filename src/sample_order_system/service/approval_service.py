from sample_order_system.model.order import OrderStatus
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository


class ApprovalService:
    """주문 승인/거절을 담당."""

    def __init__(self, sample_repository: SampleRepository, order_repository: OrderRepository):
        self.sample_repository = sample_repository
        self.order_repository = order_repository

    def reject_order(self, order_id: str) -> None:
        order = self._get_order_or_raise(order_id)
        order.status = OrderStatus.REJECTED
        self.order_repository.update(order)

    def approve_order(self, order_id: str) -> None:
        order = self._get_order_or_raise(order_id)
        sample = self.sample_repository.get(order.sample_id)

        if sample.stock < order.quantity:
            raise NotImplementedError(
                "재고 부족 시 생산 큐 등록 처리는 Cycle 4에서 구현 예정입니다."
            )

        sample.stock -= order.quantity
        order.status = OrderStatus.CONFIRMED
        self.sample_repository.update(sample)
        self.order_repository.update(order)

    def _get_order_or_raise(self, order_id: str):
        order = self.order_repository.get(order_id)
        if order is None:
            raise ValueError(f"존재하지 않는 주문입니다: {order_id}")
        return order
