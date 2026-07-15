from sample_order_system.model.order import OrderStatus
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository


class ProductionService:
    """생산 큐의 생산완료 처리를 담당."""

    def __init__(
        self,
        sample_repository: SampleRepository,
        order_repository: OrderRepository,
        production_queue: ProductionQueue,
    ):
        self.sample_repository = sample_repository
        self.order_repository = order_repository
        self.production_queue = production_queue

    def complete_current_job(self) -> None:
        job = self.production_queue.dequeue()
        if job is None:
            raise ValueError("생산 큐에 완료 처리할 작업이 없습니다.")

        sample = self.sample_repository.get(job.sample_id)
        order = self.order_repository.get(job.order_id)

        sample.stock += job.actual_qty
        sample.stock -= order.quantity
        order.status = OrderStatus.CONFIRMED

        self.sample_repository.update(sample)
        self.order_repository.update(order)
