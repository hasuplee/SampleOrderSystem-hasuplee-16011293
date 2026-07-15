from sample_order_system.model.order import OrderStatus
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository

_PENDING_STATUSES = (OrderStatus.RESERVED, OrderStatus.PRODUCING)
_COUNTED_STATUSES = (
    OrderStatus.RESERVED,
    OrderStatus.CONFIRMED,
    OrderStatus.PRODUCING,
    OrderStatus.RELEASE,
)


class MonitoringService:
    """상태별 주문 집계 및 재고 상태 계산을 담당."""

    def __init__(self, sample_repository: SampleRepository, order_repository: OrderRepository):
        self.sample_repository = sample_repository
        self.order_repository = order_repository

    def status_counts(self) -> dict:
        counts = {status.value: 0 for status in _COUNTED_STATUSES}
        for order in self.order_repository.list_all():
            if order.status in _COUNTED_STATUSES:
                counts[order.status.value] += 1
        return counts

    def stock_states(self) -> list[dict]:
        demand_by_sample = self._pending_demand_by_sample()

        rows = []
        for sample in self.sample_repository.list_all():
            demand = demand_by_sample.get(sample.sample_id, 0)

            if sample.stock == 0:
                state = "고갈"
            elif sample.stock < demand:
                state = "부족"
            else:
                state = "여유"

            ratio = 1.0 if demand == 0 else min(1.0, sample.stock / demand)
            rows.append({
                "sample_id": sample.sample_id,
                "name": sample.name,
                "stock": sample.stock,
                "pending_demand": demand,
                "state": state,
                "ratio": ratio,
            })
        return rows

    def _pending_demand_by_sample(self) -> dict:
        demand: dict = {}
        for order in self.order_repository.list_all():
            if order.status in _PENDING_STATUSES:
                demand[order.sample_id] = demand.get(order.sample_id, 0) + order.quantity
        return demand
