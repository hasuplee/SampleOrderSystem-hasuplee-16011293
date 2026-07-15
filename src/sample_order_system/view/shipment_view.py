from sample_order_system.view.order_list_view import show_order_list
from sample_order_system.view.prompts import read_index_in_range


def show_confirmed_orders(confirmed) -> None:
    show_order_list(confirmed, "출고 가능한 주문이 없습니다.")


def get_target_order_index(count: int) -> int:
    return read_index_in_range("출고할 번호 > ", count)


def show_shipment_result(order) -> None:
    print(f"출고 처리 완료. 주문번호 {order.order_id}   상태 {order.status.value}")


def show_error(message: str) -> None:
    print(f"오류: {message}")
