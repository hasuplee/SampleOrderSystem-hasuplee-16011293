from sample_order_system.view.prompts import read_positive_int, read_text


def get_new_order_input() -> dict:
    return {
        "sample_id": read_text("시료 ID > "),
        "customer_name": read_text("고객명 > "),
        "quantity": read_positive_int("주문 수량 > "),
    }


def show_order_confirmation(order) -> None:
    print("예약 접수 완료.")
    print(f"주문번호 {order.order_id}   현재 상태 {order.status.value}")


def show_error(message: str) -> None:
    print(f"오류: {message}")
