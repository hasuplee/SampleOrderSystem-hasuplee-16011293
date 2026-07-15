from sample_order_system.model.order import Order
from sample_order_system.repository.sample_repository import SampleRepository


def resolve_sample_names(orders: list[Order], sample_repository: SampleRepository) -> list[dict]:
    """주문 목록을 시료명과 함께 화면 표시용 딕셔너리 목록으로 변환한다."""
    rows = []
    for order in orders:
        sample = sample_repository.get(order.sample_id)
        rows.append({
            "order_id": order.order_id,
            "customer_name": order.customer_name,
            "sample_name": sample.name,
            "quantity": order.quantity,
        })
    return rows
