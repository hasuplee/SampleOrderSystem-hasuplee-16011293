import math

from sample_order_system.model.order import OrderStatus
from sample_order_system.model.production_job import ProductionJob
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository


class ApprovalService:
    """주문 승인/거절을 담당."""

    def __init__(
        self,
        sample_repository: SampleRepository,
        order_repository: OrderRepository,
        production_queue: ProductionQueue,
    ):
        self.sample_repository = sample_repository
        self.order_repository = order_repository
        self.production_queue = production_queue

    def reject_order(self, order_id: str) -> None:
        order = self._get_order_or_raise(order_id)
        order.status = OrderStatus.REJECTED
        self.order_repository.update(order)

    def approve_order(self, order_id: str) -> None:
        order = self._get_order_or_raise(order_id)
        sample = self.sample_repository.get(order.sample_id)

        if sample.stock < order.quantity:
            self._enqueue_production_job(order, sample)
            return

        sample.stock -= order.quantity
        order.status = OrderStatus.CONFIRMED
        self.sample_repository.update(sample)
        self.order_repository.update(order)

    def _enqueue_production_job(self, order, sample) -> None:
        shortage_qty = order.quantity - sample.stock
        actual_qty = math.ceil(shortage_qty / sample.yield_rate)
        job = ProductionJob(
            order_id=order.order_id,
            sample_id=sample.sample_id,
            shortage_qty=shortage_qty,
            actual_qty=actual_qty,
            total_time_min=sample.avg_production_time * actual_qty,
        )
        self.production_queue.enqueue(job)
        order.status = OrderStatus.PRODUCING
        self.order_repository.update(order)

    def _get_order_or_raise(self, order_id: str):
        order = self.order_repository.get(order_id)
        if order is None:
            raise ValueError(f"존재하지 않는 주문입니다: {order_id}")
        return order
