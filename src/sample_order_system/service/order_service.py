from sample_order_system.model.order import Order
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.sample_repository import SampleRepository


class OrderService:
    """시료 주문(예약) 생성을 담당."""

    def __init__(self, sample_repository: SampleRepository, order_repository: OrderRepository):
        self.sample_repository = sample_repository
        self.order_repository = order_repository

    def create_order(self, sample_id: str, customer_name: str, quantity: int) -> Order:
        if self.sample_repository.get(sample_id) is None:
            raise ValueError(f"등록되지 않은 시료 ID입니다: {sample_id}")

        order = Order(
            order_id=self.order_repository.next_order_id(),
            sample_id=sample_id,
            customer_name=customer_name,
            quantity=quantity,
        )
        self.order_repository.create(order)
        return order
